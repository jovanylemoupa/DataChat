from rest_framework import serializers


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField()
    resource_id = serializers.CharField()
    conversation_id = serializers.CharField(required=False, allow_null=True)


class MessageResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    role = serializers.CharField()
    content = serializers.CharField()
    method_explanation = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()