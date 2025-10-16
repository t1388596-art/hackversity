from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Prefetch, Count
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from .models import Conversation, Message, ConversationStats, LearningModule, LearningVideo
from .services import AIService
import json
import logging

logger = logging.getLogger(__name__)


def landing_page(request):
    """Landing page view that shows the landing page"""
    context = {
        'show_landing': True
    }
    return render(request, 'chat/home.html', context)


def learning_home(request):
    """Learning page with modules from database"""
    modules = LearningModule.objects.filter(is_active=True).prefetch_related('videos')
    context = {
        'modules': modules
    }
    return render(request, 'learning/home.html', context)


def python_tutorial(request):
    """Python tutorial page with structured learning modules"""
    return render(request, 'learning/python_tutorial.html')


def module_detail(request, slug):
    """Generic module detail view using database data"""
    module = get_object_or_404(LearningModule, slug=slug, is_active=True)
    videos = module.videos.filter(is_active=True).order_by('order')
    
    # Create video titles JSON for JavaScript
    video_titles = {video.youtube_id: video.title for video in videos}
    
    context = {
        'module': module,
        'module_title': module.title,
        'module_description': module.description,
        'module_icon': module.icon,
        'videos': videos,
        'video_titles_json': json.dumps(video_titles)
    }
    return render(request, 'learning/module_detail.html', context)


def getting_started_module(request):
    """Getting Started cybersecurity module - backwards compatibility"""
    return module_detail(request, 'getting-started')


def network_security_module(request):
    """Network Security module - backwards compatibility"""
    return module_detail(request, 'network-security')


def web_security_module(request):
    """Web Application Security module - backwards compatibility"""
    return module_detail(request, 'web-security')


def bug_bounty_module(request):
    """Bug Bounty Hunting module - backwards compatibility"""
    return module_detail(request, 'bug-bounty')


def digital_forensics_module(request):
    """Digital Forensics module - backwards compatibility"""
    return module_detail(request, 'digital-forensics')


def advanced_security_module(request):
    """Advanced Security module - backwards compatibility"""
    return module_detail(request, 'advanced-security')


@login_required
def home(request):
    """Production-safe main chat interface with robust error handling and performance optimizations"""
    try:
        # Use cached conversations for better performance
        conversations = Conversation.get_user_conversations_cached(request.user, limit=10)
        
        # Check if a specific conversation is requested
        conversation_id = request.GET.get('conversation')
        active_conversation = None
        
        if conversation_id:
            try:
                # Use select_related to avoid N+1 queries
                active_conversation = Conversation.objects.select_related('user').get(
                    id=conversation_id, user=request.user
                )
            except (Conversation.DoesNotExist, ValueError):
                logger.warning(f"Invalid conversation ID requested: {conversation_id} by user {request.user.id}")
                pass
        
        # Check if chat interface is forced (from Chat nav link)
        force_chat = request.GET.get('force_chat')
        
        # If forcing chat interface but no specific conversation, use the most recent one or create new one
        if force_chat and not active_conversation:
            if conversations:
                active_conversation = conversations[0]
            # For new users with no conversations, force_chat=1 will still show chat interface
            # but with no active_conversation, which will show the welcome message in chat layout
        
        # Get AI model information (cached)
        cache_key = f'ai_model_info_{request.user.id}'
        model_info = cache.get(cache_key)
        
        if model_info is None:
            ai_service = AIService()
            try:
                model_info = ai_service.get_model_info()
                cache.set(cache_key, model_info, timeout=3600)  # Cache for 1 hour
            except Exception as e:
                logger.error(f"Failed to get AI model info: {e}")
                model_info = {"model": "Unknown", "status": "Error"}
        model_info = ai_service.get_model_info()
        
        context = {
            'conversations': conversations,
            'active_conversation': active_conversation,
            'messages': active_conversation.messages.all() if active_conversation else [],
            'force_chat': force_chat,  # Pass this to template for logic
            'model_info': model_info,  # Add model info for display
        }
        
        # Always render the main template - no fallback that causes loading screen
        return render(request, 'chat/home.html', context)
            
    except Exception as e:
        # Even with errors, render main template with error context
        print(f"Chat view error: {e}")  # Log for debugging
        # Even with errors, try to get model info
        try:
            ai_service = AIService()
            model_info = ai_service.get_model_info()
        except:
            model_info = {'name': 'Unknown', 'provider': 'N/A', 'status': 'error'}
        
        context = {
            'conversations': [],
            'active_conversation': None,
            'messages': [],
            'force_chat': False,
            'error_message': str(e),
            'model_info': model_info,
        }
        return render(request, 'chat/home.html', context)


# Removed fallback function that was causing the loading screen in production
# The main template should always render properly with the updated static files configuration


@login_required
def conversation_detail(request, conversation_id):
    """View specific conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    conversations = Conversation.objects.filter(user=request.user)[:10]
    
    context = {
        'conversations': conversations,
        'active_conversation': conversation,
        'messages': conversation.messages.all(),
    }
    return render(request, 'chat/home.html', context)


@login_required
@csrf_exempt
def new_conversation(request):
    """Create a new conversation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conversation = Conversation.objects.create(user=request.user)
            
            # If initial message is provided, process it
            initial_message = data.get('initial_message')
            if initial_message:
                # Create user message
                user_message = Message.objects.create(
                    conversation=conversation,
                    content=initial_message,
                    is_from_user=True
                )
                
                # Generate AI response
                ai_service = AIService()
                try:
                    ai_response = ai_service.generate_response(initial_message)
                    Message.objects.create(
                        conversation=conversation,
                        content=ai_response,
                        is_from_user=False
                    )
                except Exception as e:
                    print(f"AI service error: {e}")
                    ai_response = "I'm sorry, I'm having trouble responding right now. Please try again later."
                    Message.objects.create(
                        conversation=conversation,
                        content=ai_response,
                        is_from_user=False
                    )
            
            return JsonResponse({
                'success': True,
                'conversation_id': conversation.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    else:
        # Handle GET request - redirect to home without creating conversation
        # This allows the UI to show the "new chat" interface
        return redirect('chat:home')


@login_required
@csrf_exempt
def send_message(request):
    """Send a message and get AI response"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        
        if not message_content:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get or create conversation
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        else:
            conversation = Conversation.objects.create(user=request.user)
        
        # Save user message
        user_message = Message.objects.create(
            conversation=conversation,
            content=message_content,
            is_from_user=True
        )
        
        # Generate AI response
        ai_service = AIService()
        conversation_history = conversation.messages.order_by('created_at')
        ai_response = ai_service.generate_response(message_content, conversation_history)
        
        # Save AI response
        ai_message = Message.objects.create(
            conversation=conversation,
            content=ai_response,
            is_from_user=False
        )
        
        # Update conversation title if it's the first message
        if not conversation.title:
            conversation.title = ai_service.generate_conversation_title(message_content)
            conversation.save()
        
        return JsonResponse({
            'success': True,
            'conversation_id': conversation.id,
            'user_message': {
                'id': user_message.id,
                'content': user_message.content,
                'created_at': user_message.created_at.isoformat(),
            },
            'ai_message': {
                'id': ai_message.id,
                'content': ai_message.content,
                'created_at': ai_message.created_at.isoformat(),
            },
            'conversation_title': conversation.title,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def delete_conversation(request, conversation_id):
    """Delete a conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    conversation.delete()
    # Notification removed per user request
    return redirect('chat:home')


@login_required
@csrf_exempt
def api_delete_conversation(request, conversation_id):
    """API endpoint to delete a conversation"""
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        conversation.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


class ConversationListView(ListView):
    """List all conversations for the user"""
    model = Conversation
    template_name = 'chat/conversation_list.html'
    context_object_name = 'conversations'
    paginate_by = 20
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)