from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.home, name='home'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('new/', views.new_conversation, name='new_conversation'),
    path('send/', views.send_message, name='send_message'),
    path('delete/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
    path('conversations/', views.ConversationListView.as_view(), name='conversation_list'),
    # API endpoints for AJAX calls
    path('api/conversations/', views.new_conversation, name='api_new_conversation'),
    path('api/conversations/<int:conversation_id>/messages/', views.send_message, name='api_send_message'),
    path('api/conversations/<int:conversation_id>/', views.api_delete_conversation, name='api_delete_conversation'),
    # Learning pages
    path('learning/', views.learning_home, name='learning_home'),
    path('learning/getting-started/', views.getting_started_module, name='getting_started_module'),
    path('learning/network-security/', views.network_security_module, name='network_security_module'),
    path('learning/web-security/', views.web_security_module, name='web_security_module'),
    path('learning/bug-bounty/', views.bug_bounty_module, name='bug_bounty_module'),
    path('learning/digital-forensics/', views.digital_forensics_module, name='digital_forensics_module'),
    path('learning/advanced-security/', views.advanced_security_module, name='advanced_security_module'),
    path('python-tutorial/', views.python_tutorial, name='python_tutorial'),
]