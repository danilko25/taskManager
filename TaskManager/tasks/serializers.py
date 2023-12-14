from rest_framework import serializers

from tasks.models import Category, Task


class CategorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField()

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class TaskSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    category_id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    deadline = serializers.DateTimeField()
    priority = serializers.IntegerField()
    status = serializers.CharField(max_length=100)
    creation_date = serializers.DateTimeField()

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.priority = validated_data.get('status', instance.status)
        instance.save()
        return instance