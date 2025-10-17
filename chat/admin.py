from django.contrib import admin
from django.utils.html import format_html
from .models import Conversation, Message, LearningModule, LearningVideo, PracticeLab, LabCompletion


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'created_at', 'updated_at', 'message_count']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'title']
    inlines = [MessageInline]
    readonly_fields = ('created_at', 'updated_at')
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'is_from_user', 'content_preview', 'created_at']
    list_filter = ['is_from_user', 'created_at']
    search_fields = ['content', 'conversation__user__username']
    readonly_fields = ('created_at',)
    
    def content_preview(self, obj):
        return obj.content[:100] + ('...' if len(obj.content) > 100 else '')
    content_preview.short_description = 'Content Preview'


class LearningVideoInline(admin.TabularInline):
    model = LearningVideo
    extra = 1
    fields = ('title', 'youtube_id', 'duration_minutes', 'order', 'is_active')
    ordering = ['order']


class PracticeLabInline(admin.StackedInline):
    model = PracticeLab
    extra = 0
    fields = ('title', 'slug', 'difficulty', 'lab_type', 'estimated_time_minutes', 'order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order']


@admin.register(LearningModule)
class LearningModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'icon_display', 'video_count', 'lab_count', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LearningVideoInline, PracticeLabInline]
    readonly_fields = ('created_at', 'updated_at')
    ordering = ['order', 'title']
    
    def icon_display(self, obj):
        return format_html('<i class="{}"></i> {}', obj.icon, obj.get_icon_display())
    icon_display.short_description = 'Icon'
    
    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Videos'
    
    def lab_count(self, obj):
        return obj.practice_labs.count()
    lab_count.short_description = 'Labs'


@admin.register(LearningVideo)
class LearningVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'youtube_preview', 'duration_display', 'order', 'is_active', 'created_at']
    list_filter = ['module', 'is_active', 'created_at']
    search_fields = ['title', 'module__title', 'youtube_id']
    readonly_fields = ('created_at', 'updated_at', 'youtube_url', 'embed_url')
    ordering = ['module', 'order', 'title']
    
    def youtube_preview(self, obj):
        return format_html(
            '<a href="{}" target="_blank">🎥 {}</a>',
            obj.youtube_url,
            obj.youtube_id
        )
    youtube_preview.short_description = 'YouTube'
    
    def duration_display(self, obj):
        return f"{obj.duration_minutes} min"
    duration_display.short_description = 'Duration'
    
    fieldsets = (
        ('Video Information', {
            'fields': ('module', 'title', 'order', 'is_active')
        }),
        ('YouTube Details', {
            'fields': ('youtube_id', 'duration_minutes', 'youtube_url', 'embed_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PracticeLab)
class PracticeLabAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'difficulty_badge', 'lab_type', 'time_display', 'points', 'order', 'is_active', 'created_at']
    list_filter = ['module', 'difficulty', 'lab_type', 'is_active', 'is_premium', 'created_at']
    search_fields = ['title', 'description', 'module__title']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ['module', 'order', 'title']
    
    def difficulty_badge(self, obj):
        colors = {
            'beginner': '#28a745',
            'intermediate': '#ffc107',
            'advanced': '#dc3545',
            'expert': '#343a40',
        }
        color = colors.get(obj.difficulty, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_difficulty_display().upper()
        )
    difficulty_badge.short_description = 'Difficulty'
    
    def time_display(self, obj):
        return f"{obj.estimated_time_minutes} min"
    time_display.short_description = 'Est. Time'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('module', 'title', 'slug', 'description', 'order', 'is_active')
        }),
        ('Lab Details', {
            'fields': ('difficulty', 'lab_type', 'estimated_time_minutes', 'points', 'is_premium')
        }),
        ('Learning Objectives', {
            'fields': ('objectives',),
            'description': 'Enter learning objectives, one per line'
        }),
        ('Lab Content', {
            'fields': ('instructions', 'hints', 'solution'),
            'classes': ('wide',)
        }),
        ('External Resources', {
            'fields': ('external_url', 'tools_required'),
            'classes': ('collapse',),
            'description': 'External lab URL and required tools (one per line)'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LabCompletion)
class LabCompletionAdmin(admin.ModelAdmin):
    list_display = ['user', 'lab', 'status_icon', 'score', 'attempts', 'hints_used', 'started_at', 'completed_at']
    list_filter = ['is_completed', 'lab__module', 'lab__difficulty', 'started_at', 'completed_at']
    search_fields = ['user__username', 'user__email', 'lab__title']
    readonly_fields = ('started_at',)
    ordering = ['-started_at']
    
    def status_icon(self, obj):
        if obj.is_completed:
            return format_html('<span style="color: green; font-size: 16px;">✅ Completed</span>')
        return format_html('<span style="color: orange; font-size: 16px;">🔄 In Progress</span>')
    status_icon.short_description = 'Status'
    
    fieldsets = (
        ('User & Lab', {
            'fields': ('user', 'lab')
        }),
        ('Progress', {
            'fields': ('is_completed', 'started_at', 'completed_at')
        }),
        ('Submission', {
            'fields': ('submission_notes', 'flag_submitted'),
            'classes': ('wide',)
        }),
        ('Scoring', {
            'fields': ('score', 'attempts', 'hints_used')
        }),
    )
    
    actions = ['mark_completed', 'reset_progress']
    
    def mark_completed(self, request, queryset):
        count = 0
        for completion in queryset:
            if not completion.is_completed:
                completion.mark_complete()
                count += 1
        self.message_user(request, f'{count} lab(s) marked as completed.')
    mark_completed.short_description = 'Mark selected labs as completed'
    
    def reset_progress(self, request, queryset):
        queryset.update(is_completed=False, completed_at=None, score=0)
        self.message_user(request, f'{queryset.count()} lab(s) progress reset.')
    reset_progress.short_description = 'Reset progress for selected labs'
