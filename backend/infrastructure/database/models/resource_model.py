from django.db import models


class Resource(models.Model):
    """
    Représente un fichier uploadé par un utilisateur.
    Peut être un CSV, Excel ou PDF.
    """

    class ResourceType(models.TextChoices):
        CSV = "csv", "CSV"
        PDF = "pdf", "PDF"
        EXCEL = "excel", "Excel"

    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        RUNNING = "running", "En cours"
        DONE = "done", "Terminé"
        FAILED = "failed", "Échoué"

    user = models.ForeignKey(
        "UserProfile",
        on_delete=models.CASCADE,
        related_name="resources"
    )
    name = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=10, choices=ResourceType.choices)
    file_path = models.CharField(max_length=500)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    size_bytes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "resources"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.resource_type})"