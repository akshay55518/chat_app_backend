from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    image_url = serializers.CharField(source="media_url", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "sender",
            "type",
            "content",
            "media_url",
            "image_url",
            "created_at",
        ]
