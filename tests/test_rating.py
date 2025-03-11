from rest_framework import status
from rest_framework.test import APITestCase
from groovetimeapi.models import Rating


class RatingTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up initial test data for all tests."""
        Rating.objects.create(value=5, description="Excellent")
        Rating.objects.create(value=3, description="Average")

    def test_list_ratings(self):
        """Test retrieving all ratings (GET /ratings)"""
        response = self.client.get("/ratings")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 ratings

    def test_retrieve_single_rating(self):
        """Test retrieving a single rating by ID (GET /ratings/<id>)"""
        rating = Rating.objects.first()
        response = self.client.get(f"/ratings/{rating.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], rating.value)
        self.assertEqual(response.data["description"], rating.description)

    def test_retrieve_nonexistent_rating(self):
        """Test retrieving a non-existent rating should return 404"""
        response = self.client.get(
            "/ratings/999")  # Assuming 999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_rating_should_fail(self):
        """Test that creating a rating (POST) is not allowed"""
        data = {"value": 4, "description": "Good"}
        response = self.client.post("/ratings", data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_rating_should_fail(self):
        """Test that updating a rating (PUT) is not allowed"""
        rating = Rating.objects.first()
        data = {"value": 1, "description": "Terrible"}
        response = self.client.put(
            f"/ratings/{rating.id}", data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_rating_should_fail(self):
        """Test that deleting a rating (DELETE) is not allowed"""
        rating = Rating.objects.first()
        response = self.client.delete(f"/ratings/{rating.id}")
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
