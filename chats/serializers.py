from rest_framework import serializers
from .models import Conversation, Participant
from users.models import User


class ParticipantSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Participant
        fields = ["user", "is_admin"]


class ConversationSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "type", "name", "wallpaper", "participants", "created_at"]

class CreateConversationSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["dm", "group"])
    user_ids = serializers.ListField(child=serializers.IntegerField())
    name = serializers.CharField(required=False)

