from rest_framework import serializers


class AutoModelSerializer(serializers.ModelSerializer):
    """
    自动包含所有字段的模型序列化器
    """

    class Meta:
        model = None
        fields = '__all__'
