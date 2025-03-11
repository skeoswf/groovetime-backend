from rest_framework import status
from rest_framework.test import APITestCase
from groovetimeapi.models import WeeklyGroove, GrooveSubmission, GroovetimeUser


class WeeklyGrooveTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up initial test data for all tests."""
        cls.week1 = WeeklyGroove.objects.create(
            active=True,
            title="Week 1",
            description="First weekly groove",
            start_day="2025-03-01",
            end_day="2025-03-07"
        )
        cls.week2 = WeeklyGroove.objects.create(
            active=False,
            title="Week 2",
            description="Second weekly groove",
            start_day="2025-03-08",
            end_day="2025-03-14"
        )

    def test_list_weekly_grooves(self):
        """Test retrieving all weekly grooves (GET /weeklygrooves)"""
        response = self.client.get("/weeklygrooves")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 grooves

    def test_list_active_weekly_groove(self):
        """Test retrieving only the active weekly groove (GET /weeklygrooves?active=true)"""
        response = self.client.get("/weeklygrooves?active=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return only one active groove
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]["active"])

    def test_retrieve_single_weekly_groove(self):
        """Test retrieving a single weekly groove by ID (GET /weeklygrooves/<id>)"""
        response = self.client.get(f"/weeklygrooves/{self.week1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.week1.title)

    def test_retrieve_nonexistent_weekly_groove(self):
        """Test retrieving a non-existent weekly groove should return 404"""
        response = self.client.get(
            "/weeklygrooves/999")  # Assuming 999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_weekly_groove(self):
        """Test creating a new weekly groove (POST /weeklygrooves)"""
        data = {
            "active": True,
            "title": "Week 3",
            "description": "New weekly groove",
            "startDay": "2025-03-15",
            "endDay": "2025-03-21"
        }
        response = self.client.post("/weeklygrooves", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that only one active groove exists
        active_grooves = WeeklyGroove.objects.filter(active=True)
        self.assertEqual(active_grooves.count(), 1)

    def test_update_weekly_groove(self):
        """Test updating a weekly groove (PUT /weeklygrooves/<id>)"""
        data = {
            "active": False,
            "title": "Updated Week 1",
            "description": "Updated description",
            "startDay": "2025-03-01",
            "endDay": "2025-03-07"
        }
        response = self.client.put(
            f"/weeklygrooves/{self.week1.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the update
        self.week1.refresh_from_db()
        self.assertEqual(self.week1.title, "Updated Week 1")
        self.assertFalse(self.week1.active)

    def test_update_nonexistent_weekly_groove(self):
        """Test updating a non-existent weekly groove should return 404"""
        data = {
            "active": False,
            "title": "Shouldn't work",
            "description": "Invalid",
            "startDay": "2025-03-15",
            "endDay": "2025-03-21"
        }
        response = self.client.put("/weeklygrooves/999", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_weekly_groove(self):
        """Test deleting a weekly groove (DELETE /weeklygrooves/<id>)"""
        response = self.client.delete(f"/weeklygrooves/{self.week1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify deletion
        self.assertFalse(WeeklyGroove.objects.filter(
            pk=self.week1.id).exists())
