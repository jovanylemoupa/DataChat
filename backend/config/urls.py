from django.urls import path, include

urlpatterns = [
    path("api/", include("interfaces.http.routes.api_routes")),
]
