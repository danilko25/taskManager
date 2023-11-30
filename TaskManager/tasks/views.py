from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task, Category
from tasks.serializers import TaskSerializer, CategorySerializer


# Create your views here.
class CategoryList(APIView):

    @swagger_auto_schema(operation_description="Get a list of all categories", responses={
        200: openapi.Response("List of categories", CategorySerializer(many=True))
    })
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Create a new category", request_body=CategorySerializer, responses={
        201: openapi.Response("Created category", CategorySerializer),
        400: 'Bad Request. Invalid input or missing required fields.',
    })
    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'category': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description="Get details of a particular category", responses={
        200: openapi.Response("Founded category", CategorySerializer),
        404: "Category does not exist"
    })
    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response({'category':serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Update details of a particular category", request_body=CategorySerializer, responses={
        200: openapi.Response("Updated category", CategorySerializer),
        400: 'Bad Request. Invalid input or missing required fields.',
    })
    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'category' : serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a category by id", responses={
        204: "Category was successfully deleted"
    })
    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskList(APIView):
    @swagger_auto_schema(operation_description="Get a list of all tasks", responses={
        200: openapi.Response("List of tasks", TaskSerializer(many=True))
    })
    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({'tasks': serializer.data})

    @swagger_auto_schema(operation_description="Create a new task", request_body=TaskSerializer, responses={
        201: openapi.Response("Created task", TaskSerializer),
        400: 'Bad Request. Invalid input or missing required fields.',
    })
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'task': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description="Get details of a particular task", responses={
        200: openapi.Response("Founded task", TaskSerializer),
        404: "Task does not exist"
    })
    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response({'task': serializer.data})

    @swagger_auto_schema(operation_description="Update details of a particular task", request_body=TaskSerializer, responses={
        200: openapi.Response("Updated task", TaskSerializer),
        400: 'Bad Request. Invalid input or missing required fields.',
    })
    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'task':serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a task by id", responses={
        204: "Task was successfully deleted"
    })
    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)