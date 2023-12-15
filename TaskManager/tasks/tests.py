from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from tasks.models import Category, Task
from tasks.serializers import TaskSerializer


# Create your tests here.

class TaskTests(APITestCase):

    def test_deadline_validator(self):
        category = Category.objects.create(name="test")
        data = {"id": 1, "category_id": 1, "title": "Завершити звіт", "description": "Написати та подати звіт до кінця тижня", "deadline": "2023-11-05T00:00:00Z", "priority": 3, "status": "В процесі", "creation_date": "2023-11-20T00:00:00Z"}
        serializer = TaskSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)

    def test_get_all_tasks(self):
        category = Category.objects.create(name="test")
        task = Task.objects.create(category_id=1,title="Завершити звіт", description="Написати та подати звіт до кінця тижня",deadline='2023-12-05', priority=3, status="В процесі", creation_date='2023-11-20')
        task = Task.objects.create(category_id=1,title="Second task", description="description",deadline='2023-12-04', priority=2, status="Second", creation_date='2023-11-10')

        response = self.client.get(reverse("tasks"))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["tasks"]), 2)

    def test_create_task(self):
        url = reverse("tasks")
        category = Category.objects.create(name="test")
        data = {"category_id": 1, "title": "Завершити звіт", "description": "Написати та подати звіт до кінця тижня",
                "deadline": "2023-12-05", "priority": 3, "status": "В процесі", "creation_date": "2023-11-20"}
        print((self.client.get(reverse("task-categories"))).data)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().category.id, data["category_id"])
        self.assertEqual(Task.objects.get().title, data["title"])
        self.assertEqual(Task.objects.get().description, data["description"])
        self.assertEqual(Task.objects.get().deadline.strftime("%Y-%m-%d"), data["deadline"])
        self.assertEqual(Task.objects.get().priority, data["priority"])
        self.assertEqual(Task.objects.get().status, data["status"])
        self.assertEqual(Task.objects.get().creation_date.strftime("%Y-%m-%d"), data["creation_date"])

    def test_fail_create_task(self):
        url = reverse("tasks")
        data = {"category_id": 1, "title": "Завершити звіт", "description": "Написати та подати звіт до кінця тижня",
                "deadline": "2023-12-05", "priority": 3, "status": "В процесі", "creation_date": "2023-11-20"}
        response = self.client.post(url, data, format('json'))
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_task(self):
        url = reverse("tasks", kwargs={"pk": 1})
        category = Category.objects.create(name="test")
        task = Task.objects.create(category_id=1,title="Завершити звіт", description="Написати та подати звіт до кінця тижня",deadline='2023-12-05', priority=3, status="В процесі", creation_date='2023-11-20')
        response = self.client.get(url)
        print(response.data)
        print(Task.objects.get().category.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().category.id, response.data["task"]["id"])
        self.assertEqual(Task.objects.get().title, response.data["task"]["title"])
        self.assertEqual(Task.objects.get().description, response.data["task"]["description"])
        self.assertEqual(Task.objects.get().priority, response.data["task"]["priority"])
        self.assertEqual(Task.objects.get().status, response.data["task"]["status"])


    def test_fail_get_task(self):
            url = reverse("tasks", kwargs={"pk": 1})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task(self):
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        category = Category.objects.create(name="test")
        task = Task.objects.create(category_id=1,title="Завершити звіт", description="Написати та подати звіт до кінця тижня",deadline='2023-12-05', priority=3, status="В процесі", creation_date='2023-11-20')
        url = reverse("tasks", kwargs={"pk": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse("tasks"))
        self.assertEqual(len(response.data["tasks"]), 0)

    def test_fail_delete_category(self):
        #delete can only superuser
        category = Category.objects.create(name="test")
        task = Task.objects.create(category_id=1, title="Завершити звіт",
                                   description="Написати та подати звіт до кінця тижня", deadline='2023-12-05',
                                   priority=3, status="В процесі", creation_date='2023-11-20')
        url = reverse("tasks", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryTests(APITestCase):

    def test_get_all_categories(self):
        category = Category.objects.create(name="test")
        category2 = Category.objects.create(name="second")
        response = self.client.get(reverse("task-categories"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["categories"]), 2)

    def test_create_category(self):
        url = reverse("task-categories")
        data = {"name":"test"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, "test")

    def test_fail_create_category(self):
        url = reverse("task-categories")
        response = self.client.post(url, {}, format('json'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response =  self.client.get(url)
        self.assertEqual(len(response.data["categories"]), 0)


    def test_get_category(self):
        url = reverse("task-categories", kwargs={"pk": 1})
        category1 = Category.objects.create(name="test")
        response = self.client.get(url)
        self.assertEqual(response.data['category']['name'], category1.name)
        self.assertEqual(response.data['category']['id'], category1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_get_category(self):
        url = reverse("task-categories", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_category(self):
        url = reverse("task-categories", kwargs={"pk": 1})
        category = Category.objects.create(name="Test Category")
        data = {"name": "Updated Category"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.data["category"]["name"], data["name"])
        self.assertEqual(response.data["category"]["id"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_update_category(self):
        url = reverse("task-categories", kwargs={"pk": 1})
        category = Category.objects.create(name="Test Category")
        data = {"unknown_field": "Updated Category"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_category(self):
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        category = Category.objects.create(name="Test Category")
        url = reverse("task-categories", kwargs={"pk": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse("task-categories"))
        self.assertEqual(len(response.data["categories"]), 0)

    def test_fail_delete_category(self):
        #delete can only superuser
        category = Category.objects.create(name="Test Category")
        url = reverse("task-categories", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


