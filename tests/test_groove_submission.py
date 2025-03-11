from rest_framework import status
from rest_framework.test import APITestCase
from groovetimeapi.models import WeeklyGroove, GrooveSubmission, GroovetimeUser


class GrooveSubmissionTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up initial test data for all tests."""
        cls.user = GroovetimeUser.objects.create(
            uid="user_123",
            profile_picture="http://example.com/pic.jpg",
            bio="Test user"
        )
        cls.weekly_groove = WeeklyGroove.objects.create(
            active=True,
            title="Week 1",
            description="First weekly groove",
            start_day="2025-03-01",
            end_day="2025-03-07"
        )
        cls.submission1 = GrooveSubmission.objects.create(
            weekly_groove=cls.weekly_groove,
            submitted_by=cls.user,
            video_url="http://example.com/video1.mp4",
            description="First submission",
            average_rating=4.5
        )

    def test_list_groove_submissions(self):
        """Test retrieving all groove submissions (GET /groovesubmissions)"""
        response = self.client.get("/groovesubmissions")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return 1 submission

    def test_list_submissions_by_weekly_groove(self):
        """Test retrieving submissions for a specific Weekly Groove (GET /groovesubmissions?weekly_groove=<id>)"""
        response = self.client.get(
            f"/groovesubmissions?weekly_groove={self.weekly_groove.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_submissions_for_active_weekly_groove(self):
        """Test retrieving submissions for the active Weekly Groove (GET /groovesubmissions?active=true)"""
        response = self.client.get("/groovesubmissions?active=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_single_submission(self):
        """Test retrieving a single submission by ID (GET /groovesubmissions/<id>)"""
        response = self.client.get(f"/groovesubmissions/{self.submission1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"],
                         self.submission1.description)

    def test_retrieve_nonexistent_submission(self):
        """Test retrieving a non-existent submission should return 404"""
        response = self.client.get(
            "/groovesubmissions/999")  # Assuming 999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_submission(self):
        """Test creating a new groove submission (POST /groovesubmissions)"""
        data = {
            "weeklyGroove": self.weekly_groove.id,
            "submittedBy": self.user.id,
            "videoURL": "http://example.com/video2.mp4",
            "description": "New submission"
        }
        response = self.client.post("/groovesubmissions", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_submission_exceeding_limit(self):
        """Test creating more than 3 submissions for a single Weekly Groove should fail"""
        # Create two more submissions to reach the limit
        GrooveSubmission.objects.create(
            weekly_groove=self.weekly_groove,
            submitted_by=self.user,
            video_url="http://example.com/video3.mp4",
            description="Second submission"
        )
        GrooveSubmission.objects.create(
            weekly_groove=self.weekly_groove,
            submitted_by=self.user,
            video_url="http://example.com/video4.mp4",
            description="Third submission"
        )

        # Attempt to create a fourth submission (should fail)
        data = {
            "weeklyGroove": self.weekly_groove.id,
            "submittedBy": self.user.id,
            "videoURL": "http://example.com/video5.mp4",
            "description": "Should fail"
        }
        response = self.client.post("/groovesubmissions", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_submission(self):
        """Test updating a submission's description (PUT /groovesubmissions/<id>)"""
        data = {"description": "Updated description"}
        response = self.client.put(
            f"/groovesubmissions/{self.submission1.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the update
        self.submission1.refresh_from_db()
        self.assertEqual(self.submission1.description, "Updated description")

    def test_update_nonexistent_submission(self):
        """Test updating a non-existent submission should return 404"""
        data = {"description": "Shouldn't work"}
        response = self.client.put(
            "/groovesubmissions/999", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_submission(self):
        """Test deleting a submission (DELETE /groovesubmissions/<id>)"""
        response = self.client.delete(
            f"/groovesubmissions/{self.submission1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify deletion
        self.assertFalse(GrooveSubmission.objects.filter(
            pk=self.submission1.id).exists())

    def test_delete_nonexistent_submission(self):
        """Test deleting a non-existent submission should return 404"""
        response = self.client.delete("/groovesubmissions/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
