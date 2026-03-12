from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ResourceUploadView(APIView):
    def post(self, request):
        return Response({"message": "TODO"}, status=status.HTTP_501_NOT_IMPLEMENTED)


class ResourceListView(APIView):
    def get(self, request):
        return Response([], status=status.HTTP_200_OK)


class ChatView(APIView):
    def post(self, request):
        return Response({"message": "TODO"}, status=status.HTTP_501_NOT_IMPLEMENTED)


class ConversationListView(APIView):
    def get(self, request):
        return Response([], status=status.HTTP_200_OK)


class ConversationDetailView(APIView):
    def get(self, request, conversation_id):
        return Response({}, status=status.HTTP_200_OK)
