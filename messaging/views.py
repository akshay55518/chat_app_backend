from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Message
from chats.models import Conversation
from .serializers import MessageSerializer


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        messages = Message.objects.filter(
            conversation_id=conversation_id
        ).order_by("-created_at")[:50]

        return Response(MessageSerializer(messages, many=True).data)

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        content = request.data.get("content", "")
        image_url = request.data.get("image_url")
        message_type = "image" if image_url else "text"

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content,
            type=message_type,
            media_url=image_url if image_url else None,
        )

        return Response(MessageSerializer(message).data, status=201)
