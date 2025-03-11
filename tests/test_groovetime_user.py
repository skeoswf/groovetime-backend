from rest_framework import status
from rest_framework.test import APITestCase
from groovetimeapi.models import GroovetimeUser
from datetime import datetime


class GroovetimeUserTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up initial test data for all tests."""
        cls.user1 = GroovetimeUser.objects.create(
            uid="user_123",
            profile_picture="http://example.com/pic1.jpg",
            bio="I love music!",
            groove_points=50.0,
            grooves_won=2,
            admin=False
        )
        cls.user2 = GroovetimeUser.objects.create(
            uid="admin_456",
            profile_picture="http://example.com/pic2.jpg",
            bio="Admin user",
            groove_points=100.0,
            grooves_won=5,
            admin=True
        )

    def test_list_users(self):
        """Test retrieving all users (GET /groovetimeusers)"""
        response = self.client.get("/groovetimeusers")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return both users

    def test_list_admin_users(self):
        """Test retrieving only admin users (GET /groovetimeusers?admin=True)"""
        response = self.client.get("/groovetimeusers?admin=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return only the admin user
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]["admin"])

    def test_retrieve_single_user(self):
        """Test retrieving a single user by ID (GET /groovetimeusers/<id>)"""
        response = self.client.get(f"/groovetimeusers/{self.user1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], self.user1.uid)
        self.assertEqual(response.data["bio"], self.user1.bio)

    def test_retrieve_nonexistent_user(self):
        """Test retrieving a non-existent user should return 404"""
        response = self.client.get(
            "/groovetimeusers/999")  # Assuming 999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self):
        """Test creating a new user (POST /groovetimeusers)"""
        data = {
            "uid": "new_user_789",
            "profilePicture": "http://example.com/new_pic.jpg",
            "bio": "New user here!"
        }
        response = self.client.post("/groovetimeusers", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["uid"], "new_user_789")

    def test_update_user(self):
        """Test updating a user's profile picture & bio (PUT /groovetimeusers/<id>)"""
        data = {
            "profilePicture": "http://example.com/updated_pic.jpg",
            "bio": "Updated bio"
        }
        response = self.client.put(
            f"/groovetimeusers/{self.user1.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the update
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.profile_picture,
                         "http://example.com/updated_pic.jpg")
        self.assertEqual(self.user1.bio, "Updated bio")

    def test_update_nonexistent_user(self):
        """Test updating a non-existent user should return 404"""
        data = {
            "profilePicture": "http://example.com/fail.jpg",
            "bio": "Shouldn't work"
        }
        response = self.client.put("/groovetimeusers/999", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        """Test deleting a user (DELETE /groovetimeusers/<id>)"""
        response = self.client.delete(f"/groovetimeusers/{self.user1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify deletion
        self.assertFalse(GroovetimeUser.objects.filter(
            pk=self.user1.id).exists())
