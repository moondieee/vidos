from rest_framework import serializers

from users.models import User


class UserGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'full_name',
            'company',
            'crm'
        )
        read_only_fields = fields
