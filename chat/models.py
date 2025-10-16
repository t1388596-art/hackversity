from django.db import models
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
import hashlib

User = get_user_model()


class Conversation(models.Model):
    """Model to store chat conversations with performance optimizations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=200, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    message_count = models.PositiveIntegerField(default=0)  # Denormalized count for performance
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at'], name='conv_user_updated_idx'),
            models.Index(fields=['user', '-created_at'], name='conv_user_created_idx'),
            models.Index(fields=['-updated_at'], name='conv_updated_idx'),
        ]
    
    def __str__(self):
        return f"Conversation {self.id} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        # Only try to set title if the conversation already exists (has a primary key)
        if not self.title and self.pk and self.messages.exists():
            # Set title to first user message (truncated)
            first_message = self.messages.filter(is_from_user=True).first()
            if first_message:
                self.title = first_message.content[:50] + ('...' if len(first_message.content) > 50 else '')
        
        # Invalidate cache when saving
        self.invalidate_cache()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Invalidate cache when deleting
        self.invalidate_cache()
        super().delete(*args, **kwargs)
    
    def invalidate_cache(self):
        """Invalidate related cache entries"""
        cache_keys = [
            f'conversation_{self.pk}',
            f'user_conversations_{self.user_id}',
            f'conversation_messages_{self.pk}',
        ]
        cache.delete_many(cache_keys)
    
    def get_messages_cached(self):
        """Get messages with caching"""
        cache_key = f'conversation_messages_{self.pk}'
        messages = cache.get(cache_key)
        
        if messages is None:
            messages = list(self.messages.select_related().all())
            cache.set(cache_key, messages, timeout=300)  # 5 minutes
        
        return messages
    
    def update_message_count(self):
        """Update denormalized message count"""
        self.message_count = self.messages.count()
        self.save(update_fields=['message_count'])
    
    @classmethod
    def get_user_conversations_cached(cls, user, limit=20):
        """Get user conversations with caching"""
        cache_key = f'user_conversations_{user.id}_{limit}'
        conversations = cache.get(cache_key)
        
        if conversations is None:
            conversations = list(
                cls.objects.filter(user=user)
                .select_related('user')
                .prefetch_related('messages')
                .order_by('-updated_at')[:limit]
            )
            cache.set(cache_key, conversations, timeout=600)  # 10 minutes
        
        return conversations


class Message(models.Model):
    """Model to store individual messages in conversations with performance optimizations"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_from_user = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    content_hash = models.CharField(max_length=64, blank=True, db_index=True)  # For deduplication
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at'], name='msg_conv_time_idx'),
            models.Index(fields=['conversation', 'is_from_user'], name='msg_conv_user_idx'),
            models.Index(fields=['created_at'], name='msg_created_idx'),
            models.Index(fields=['content_hash'], name='msg_hash_idx'),
        ]
    
    def save(self, *args, **kwargs):
        # Generate content hash for deduplication
        if not self.content_hash:
            self.content_hash = hashlib.sha256(self.content.encode()).hexdigest()
        
        # Update conversation's updated_at and message count
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Update conversation timestamp and count
            self.conversation.updated_at = self.created_at
            self.conversation.update_message_count()
            
            # Invalidate conversation cache
            self.conversation.invalidate_cache()
    
    def delete(self, *args, **kwargs):
        conversation = self.conversation
        super().delete(*args, **kwargs)
        
        # Update conversation message count and cache
        conversation.update_message_count()
        conversation.invalidate_cache()
    
    def __str__(self):
        sender = "User" if self.is_from_user else "AI"
        return f"{sender}: {self.content[:50]}..."
    
    @classmethod
    def get_recent_messages(cls, conversation_id, limit=50):
        """Get recent messages for a conversation with optimization"""
        return cls.objects.filter(
            conversation_id=conversation_id
        ).select_related('conversation').order_by('-created_at')[:limit]


class ConversationStats(models.Model):
    """Model to store conversation statistics for performance monitoring"""
    date = models.DateField(auto_now_add=True, db_index=True)
    total_conversations = models.PositiveIntegerField(default=0)
    total_messages = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    avg_messages_per_conversation = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ['date']
        ordering = ['-date']
    
    @classmethod
    def update_daily_stats(cls):
        """Update daily statistics"""
        from django.db.models import Count, Avg
        today = timezone.now().date()
        
        stats, created = cls.objects.get_or_create(date=today)
        
        # Calculate statistics
        total_conversations = Conversation.objects.count()
        total_messages = Message.objects.count()
        active_users = User.objects.filter(conversations__isnull=False).distinct().count()
        
        avg_messages = Conversation.objects.aggregate(
            avg=Avg('message_count')
        )['avg'] or 0.0
        
        # Update stats
        stats.total_conversations = total_conversations
        stats.total_messages = total_messages
        stats.active_users = active_users
        stats.avg_messages_per_conversation = avg_messages
        stats.save()
        
        return stats
    
    @classmethod
    def get_recent_messages(cls, conversation_id, limit=50):
        """Get recent messages for a conversation with optimization"""
        return cls.objects.filter(
            conversation_id=conversation_id
        ).select_related('conversation').order_by('-timestamp')[:limit]


class LearningModule(models.Model):
    """Model to store learning modules"""
    ICON_CHOICES = [
        ('fas fa-seedling', 'Seedling (Getting Started)'),
        ('fas fa-network-wired', 'Network (Network Security)'),
        ('fas fa-globe', 'Globe (Web Security)'),
        ('fas fa-bug', 'Bug (Bug Bounty)'),
        ('fas fa-search', 'Search (Digital Forensics)'),
        ('fas fa-shield-alt', 'Shield (Advanced Security)'),
        ('fas fa-laptop-code', 'Laptop Code'),
        ('fas fa-lock', 'Lock'),
        ('fas fa-key', 'Key'),
        ('fas fa-eye', 'Eye'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fas fa-seedling')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class LearningVideo(models.Model):
    """Model to store individual learning videos"""
    module = models.ForeignKey(LearningModule, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=20, help_text="YouTube video ID (e.g., 'ePD7cLWkt-E')")
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
        unique_together = ['module', 'order']
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"
    
    @property
    def youtube_url(self):
        return f"https://youtu.be/{self.youtube_id}"
    
    @property
    def embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_id}"


class PracticeLab(models.Model):
    """Model to store practice labs for hands-on learning"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    LAB_TYPE_CHOICES = [
        ('interactive', 'Interactive Exercise'),
        ('ctf', 'Capture The Flag'),
        ('scenario', 'Real-world Scenario'),
        ('quiz', 'Knowledge Quiz'),
        ('coding', 'Coding Challenge'),
        ('network', 'Network Lab'),
        ('webapp', 'Web Application Lab'),
    ]
    
    module = models.ForeignKey(LearningModule, on_delete=models.CASCADE, related_name='practice_labs')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(help_text="Brief description of the lab")
    objectives = models.TextField(help_text="Learning objectives (one per line)")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    lab_type = models.CharField(max_length=20, choices=LAB_TYPE_CHOICES, default='interactive')
    
    # Lab content
    instructions = models.TextField(help_text="Step-by-step lab instructions")
    hints = models.TextField(blank=True, help_text="Hints for students (optional)")
    solution = models.TextField(blank=True, help_text="Lab solution/walkthrough (optional)")
    
    # External resources
    external_url = models.URLField(blank=True, help_text="External lab URL (e.g., TryHackMe, HackTheBox)")
    tools_required = models.TextField(blank=True, help_text="Required tools (one per line)")
    
    # Metadata
    estimated_time_minutes = models.PositiveIntegerField(default=30, help_text="Estimated completion time")
    points = models.PositiveIntegerField(default=10, help_text="Points awarded for completion")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False, help_text="Requires premium access")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['module', 'order', 'title']
        unique_together = ['module', 'slug']
        indexes = [
            models.Index(fields=['module', 'is_active']),
            models.Index(fields=['difficulty']),
            models.Index(fields=['lab_type']),
        ]
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"
    
    @property
    def difficulty_badge_color(self):
        """Return color class for difficulty badge"""
        colors = {
            'beginner': 'success',
            'intermediate': 'warning',
            'advanced': 'danger',
            'expert': 'dark',
        }
        return colors.get(self.difficulty, 'secondary')
    
    @property
    def objectives_list(self):
        """Return objectives as a list"""
        return [obj.strip() for obj in self.objectives.split('\n') if obj.strip()]
    
    @property
    def tools_list(self):
        """Return tools as a list"""
        return [tool.strip() for tool in self.tools_required.split('\n') if tool.strip()]


class LabCompletion(models.Model):
    """Track user progress on practice labs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_completions')
    lab = models.ForeignKey(PracticeLab, on_delete=models.CASCADE, related_name='completions')
    
    # Progress tracking
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    # Submission
    submission_notes = models.TextField(blank=True, help_text="User's notes or solution")
    flag_submitted = models.CharField(max_length=200, blank=True, help_text="CTF flag if applicable")
    
    # Scoring
    score = models.PositiveIntegerField(default=0, help_text="Score earned (0-100)")
    attempts = models.PositiveIntegerField(default=0)
    hints_used = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-started_at']
        unique_together = ['user', 'lab']
        indexes = [
            models.Index(fields=['user', 'is_completed']),
            models.Index(fields=['lab', 'is_completed']),
        ]
    
    def __str__(self):
        status = "✅" if self.is_completed else "🔄"
        return f"{status} {self.user.username} - {self.lab.title}"
    
    def mark_complete(self, score=100):
        """Mark lab as completed"""
        self.is_completed = True
        self.completed_at = timezone.now()
        self.score = score
        self.save()
