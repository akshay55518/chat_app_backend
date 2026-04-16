from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Conversation(models.Model):
    CONVERSATION_TYPE = (
        ("dm", "Direct Message"),
        ("group", "Group"),
    )

    type = models.CharField(max_length=10, choices=CONVERSATION_TYPE)

    name = models.CharField(max_length=255, blank=True, null=True)
    wallpaper = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.type}"

class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="participants"
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "conversation")