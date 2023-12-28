from rest_framework import serializers

from ..models import Website


class WebsiteGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = (
            'user',
            'name',
            'url',
            'description',
        )
        read_only_fields = fields
