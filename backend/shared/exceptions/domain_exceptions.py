class ResourceNotFoundError(Exception):
    def __init__(self, resource_id: str):
        super().__init__(f"Ressource introuvable : {resource_id}")


class InvalidFileTypeError(Exception):
    def __init__(self, file_type: str):
        super().__init__(f"Type de fichier non supporté : {file_type}")


class ConversationNotFoundError(Exception):
    def __init__(self, conversation_id: str):
        super().__init__(f"Conversation introuvable : {conversation_id}")
