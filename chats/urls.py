from django.urls import path
from .views import (
    CreateConversationView,
    ConversationListView,
    ConversationDetailView,
    AddMemberView,
    RemoveMemberView,
)

urlpatterns = [
    path("", ConversationListView.as_view()),
    path("create", CreateConversationView.as_view()),
    path("<int:conversation_id>", ConversationDetailView.as_view()),
    path("<int:conversation_id>/add-member", AddMemberView.as_view()),
    path("<int:conversation_id>/remove-member/<int:user_id>", RemoveMemberView.as_view()),
]