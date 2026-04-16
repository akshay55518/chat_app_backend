from django.db import models
from django.conf import settings
from chats.models import Conversation

User = settings.AUTH_USER_MODEL


class Message(models.Model):
    MESSAGE_TYPE = (
        ("text", "Text"),
        ("image", "Image"),
        ("file", "File"),
        ("audio", "Audio"),
    )

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    type = models.CharField(max_length=10, choices=MESSAGE_TYPE, default="text")

    content = models.TextField(blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)

    is_edited = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} -> {self.conversation}"

class MessageRead(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("message", "user")

class UserConversationState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

    last_read_message = models.ForeignKey(
        Message, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        unique_together = ("user", "conversation")