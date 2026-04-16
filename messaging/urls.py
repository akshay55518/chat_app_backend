from django.urls import path
from .views import MessageListView, SendMessageView

urlpatterns = [
    path("<int:conversation_id>", MessageListView.as_view()),
    path("<int:conversation_id>/send", SendMessageView.as_view()),
]