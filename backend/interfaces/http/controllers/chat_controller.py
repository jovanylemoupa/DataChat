from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from application.use_cases.ask_question import AskQuestionUseCase
from application.dto.message_dto import QuestionDTO
from infrastructure.database.repositories.django_resource_repository import DjangoResourceRepository
from infrastructure.database.repositories.django_conversation_repository import DjangoConversationRepository
from infrastructure.database.repositories.django_message_repository import DjangoMessageRepository
from infrastructure.ai.agent.graph import agent_graph
from interfaces.http.serializers.message_serializer import QuestionSerializer, MessageResponseSerializer
from shared.exceptions.domain_exceptions import ResourceNotFoundError


class ChatView(APIView):

    def post(self, request):
        # 1. Valider les données
        serializer = QuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Construire le DTO
        dto = QuestionDTO(
            question=serializer.validated_data["question"],
            resource_id=serializer.validated_data["resource_id"],
            conversation_id=serializer.validated_data.get("conversation_id"),
            user_id=request.user_id,
        )

        # 3. Instancier le use case avec injection de dépendances
        use_case = AskQuestionUseCase(
            conversation_repository=DjangoConversationRepository(),
            message_repository=DjangoMessageRepository(),
            resource_repository=DjangoResourceRepository(),
            agent=agent_graph,
        )

        # 4. Exécuter
        try:
            result = use_case.execute(dto)
        except ResourceNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        # 5. Retourner la réponse
        response_serializer = MessageResponseSerializer(result.__dict__)
        return Response(response_serializer.data, status=status.HTTP_200_OK)