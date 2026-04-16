from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Conversation, Participant
from .serializers import ConversationSerializer, CreateConversationSerializer
from users.models import User

class CreateConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateConversationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data

        conversation = Conversation.objects.create(
            type=data["type"],
            name=data.get("name")
        )

        # add creator
        Participant.objects.create(
            user=request.user,
            conversation=conversation,
            is_admin=True
        )

        # add others
        users = User.objects.filter(id__in=data["user_ids"])
        for user in users:
            Participant.objects.get_or_create(
                user=user,
                conversation=conversation
            )

        return Response(ConversationSerializer(conversation).data, status=201)

class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversations = Conversation.objects.filter(
            participants__user=request.user
        ).distinct()

        data = ConversationSerializer(conversations, many=True).data
        return Response(data)

class ConversationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id)

        return Response(ConversationSerializer(conversation).data)

class AddMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        user_id = request.data.get("user_id")

        conversation = get_object_or_404(Conversation, id=conversation_id)
        user = get_object_or_404(User, id=user_id)

        Participant.objects.get_or_create(
            user=user,
            conversation=conversation
        )

        return Response({"message": "User added"})

class RemoveMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, conversation_id, user_id):
        Participant.objects.filter(
            conversation_id=conversation_id,
            user_id=user_id
        ).delete()

        return Response({"message": "User removed"})