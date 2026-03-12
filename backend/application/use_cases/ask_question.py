from application.dto.message_dto import QuestionDTO, MessageResponseDTO
from domain.models.conversation import Conversation
from domain.models.message import Message
from domain.repositories.conversation_repository import ConversationRepository
from domain.repositories.message_repository import MessageRepository
from domain.repositories.resource_repository import ResourceRepository
from domain.entities.message_role import MessageRole
from shared.exceptions.domain_exceptions import ResourceNotFoundError


class AskQuestionUseCase:

    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
        resource_repository: ResourceRepository,
        agent,  # infrastructure/ai/agent/graph.py
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
        self.resource_repository = resource_repository
        self.agent = agent

    def execute(self, dto: QuestionDTO) -> MessageResponseDTO:
        # 1. Vérifier que le fichier existe
        resource = self.resource_repository.find_by_id(dto.resource_id)
        if resource is None:
            raise ResourceNotFoundError(dto.resource_id)

        # 2. Récupérer ou créer la conversation
        conversation = self._get_or_create_conversation(dto, resource)

        # 3. Sauvegarder le message utilisateur
        user_message = Message(
            id=None,
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=dto.question,
        )
        self.message_repository.save(user_message)

        # 4. Charger l'historique de conversation
        history = self.message_repository.find_by_conversation(conversation.id)

        # 5. Appeler l'agent LangGraph
        result = self.agent.invoke({
            "question": dto.question,
            "resource_id": dto.resource_id,
            "resource_type": resource.resource_type.value,
            "conversation_history": [
                {"role": m.role.value, "content": m.content}
                for m in history
            ],
            "dataframe": None,
            "chunks": [],
            "route": "",
            "analysis_result": None,
            "retrieved_context": [],
            "needs_clarification": False,
            "clarification_question": None,
            "final_response": None,
            "method_explanation": None,
            "error": None,
        })

        # 6. Sauvegarder la réponse de l'agent
        agent_message = Message(
            id=None,
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=result.get("final_response", ""),
            method_explanation=result.get("method_explanation"),
        )
        saved = self.message_repository.save(agent_message)

        # 7. Retourner le DTO de réponse
        return MessageResponseDTO(
            id=saved.id,
            role=saved.role.value,
            content=saved.content,
            method_explanation=saved.method_explanation,
            created_at=saved.created_at,
        )

    def _get_or_create_conversation(self, dto: QuestionDTO, resource) -> Conversation:
        """Charge la conversation existante ou en crée une nouvelle."""
        if dto.conversation_id:
            return self.conversation_repository.find_by_id(dto.conversation_id)

        conversation = Conversation(
            id=None,
            user_id=dto.user_id,
            resource_id=dto.resource_id,
            title=f"Analyse de {resource.name}",
        )
        return self.conversation_repository.save(conversation)