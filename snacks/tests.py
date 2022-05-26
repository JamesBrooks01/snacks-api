from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Snack


class SnackTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_snack = Snack.objects.create(
            title="rake",
            purchaser=testuser1,
            description="Better for collecting leaves than a shovel.",
        )
        test_snack.save()

    def test_snacks_model(self):
        snack = Snack.objects.get(id=1)
        actual_purchaser = str(snack.purchaser)
        actual_title = str(snack.title)
        actual_description = str(snack.description)
        self.assertEqual(actual_purchaser, "testuser1")
        self.assertEqual(actual_title, "rake")
        self.assertEqual(
            actual_description, "Better for collecting leaves than a shovel."
        )

    def test_get_snack_list(self):
        url = reverse("snack_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        snacks = response.data
        self.assertEqual(len(snacks), 1)
        self.assertEqual(snacks[0]["title"], "rake")

    def test_get_snack_by_id(self):
        url = reverse("snack_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        snacks = response.data
        self.assertEqual(snacks["title"], "rake")

    def test_create_snack(self):
        url = reverse("snack_list")
        data = {"purchaser": 1, "title": "spoon", "description": "good for cereal and soup"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        snacks = Snack.objects.all()
        self.assertEqual(len(snacks), 2)
        self.assertEqual(Snack.objects.get(id=2).title, "spoon")

    def test_update_snack(self):
        url = reverse("snack_detail", args=(1,))
        data = {
            "purchaser": 1,
            "title": "rake",
            "description": "pole with a crossbar toothed like a comb.",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        snack = Snack.objects.get(id=1)
        self.assertEqual(snack.title, data["title"])
        self.assertEqual(snack.purchaser.id, data["purchaser"])
        self.assertEqual(snack.description, data["description"])

    def test_delete_snack(self):
        url = reverse("snack_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        snacks = Snack.objects.all()
        self.assertEqual(len(snacks), 0)