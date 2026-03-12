from django.db import models


class UserProfile(models.Model):
    """
    Représente un utilisateur authentifié via Keycloak.
    keycloak_id = le 'sub' du token JWT Keycloak.
    """
    keycloak_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_profiles"

    def __str__(self):
        return self.email