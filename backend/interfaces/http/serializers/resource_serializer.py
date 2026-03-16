from rest_framework import serializers


class ResourceUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class ResourceResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    resource_type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    size_bytes = serializers.IntegerField()
    created_at = serializers.DateTimeField()

    def get_resource_type(self, obj):
        val = obj.get("resource_type") if isinstance(obj, dict) else obj.resource_type
        return val.value if hasattr(val, "value") else val

    def get_status(self, obj):
        val = obj.get("status") if isinstance(obj, dict) else obj.status
        return val.value if hasattr(val, "value") else val
