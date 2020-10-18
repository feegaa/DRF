from rest_framework import serializers
from api.models import PostModel

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PostModel
        # fields = ['title', 'content']
        fields = '__all__'

class PostSerializer(serializers.Serializer):
    id      = serializers.IntegerField(read_only=True)
    title   = serializers.CharField(max_length=10)
    content = serializers.CharField(max_length=10)
    date    = serializers.DateField(read_only=True)

    def create(self, validated_data):
        return PostModel.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.title   = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        # instance.date    = validated_data.get('date', instance.date)
        instance.save()
        return instance


    