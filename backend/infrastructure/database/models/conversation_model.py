from django.db import models


class Conversation(models.Model):
    """
    Représente une session de chat entre un utilisateur et l'agent IA.
    Chaque conversation est liée à un fichier (Resource).
    """
    user = models.ForeignKey(
        "UserProfile",
        on_delete=models.CASCADE,
        related_name="conversations"
    )
    resource = models.ForeignKey(
        "Resource",
        on_delete=models.CASCADE,
        related_name="conversations"
    )
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "conversations"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.title} — {self.user.email}"