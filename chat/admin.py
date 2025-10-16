from django.contrib import admin
from django.utils.html import format_html
from .models import Conversation, Message, LearningModule, LearningVideo


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


@admin.register(LearningModule)
class LearningModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'icon_display', 'video_count', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LearningVideoInline]
    readonly_fields = ('created_at', 'updated_at')
    ordering = ['order', 'title']
    
    def icon_display(self, obj):
        return format_html('<i class="{}"></i> {}', obj.icon, obj.get_icon_display())
    icon_display.short_description = 'Icon'
    
    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Videos'


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