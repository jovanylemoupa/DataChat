from django.urls import path
from interfaces.http.controllers.resource_controller import ResourceUploadView, ResourceListView
from interfaces.http.controllers.chat_controller import ChatView
from interfaces.http.controllers.conversation_controller import ConversationListView, ConversationDetailView

urlpatterns = [
    # Resources
    path("resources/", ResourceListView.as_view(), name="resource-list"),
    path("resources/upload/", ResourceUploadView.as_view(), name="resource-upload"),

    # Chat
    path("chat/", ChatView.as_view(), name="chat"),

    # Conversations
    path("conversations/", ConversationListView.as_view(), name="conversation-list"),
    path("conversations/<str:conversation_id>/", ConversationDetailView.as_view(), name="conversation-detail"),
]
