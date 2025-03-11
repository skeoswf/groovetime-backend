from rest_framework import status
from rest_framework.test import APITestCase
from groovetimeapi.models import WeeklyGroove, GrooveSubmission, GroovetimeUser, Rating, GrooveSubmissionRating


class GrooveSubmissionRatingTests(APITestCase):

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
        cls.submission = GrooveSubmission.objects.create(
            weekly_groove=cls.weekly_groove,
            submitted_by=cls.user,
            video_url="http://example.com/video.mp4",
            description="Test submission",
            average_rating=None
        )
        cls.rating_5 = Rating.objects.create(value=5, description="Excellent")
        cls.rating_3 = Rating.objects.create(value=3, description="Average")

    def test_list_groove_submission_ratings(self):
        """Test retrieving all groove submission ratings (GET /groovesubmissionratings)"""
        response = self.client.get("/groovesubmissionratings")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_ratings_by_groove_submission(self):
        """Test retrieving ratings for a specific submission (GET /groovesubmissionratings?groove_submission=<id>)"""
        response = self.client.get(
            f"/groovesubmissionratings?groove_submission={self.submission.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_rating(self):
        """Test retrieving a single rating by ID (GET /groovesubmissionratings/<id>)"""
        rating_entry = GrooveSubmissionRating.objects.create(
            groove_submission=self.submission,
            user_submitted=self.user,
            rating_value=self.rating_5
        )
        response = self.client.get(
            f"/groovesubmissionratings/{rating_entry.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating_value"], self.rating_5.id)

    def test_create_groove_submission_rating(self):
        """Test creating a new rating for a submission (POST /groovesubmissionratings)"""
        data = {
            "grooveSubmission": self.submission.id,
            "userSubmitted": self.user.id,
            "ratingValue": self.rating_5.id
        }
        response = self.client.post(
            "/groovesubmissionratings", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_duplicate_rating_should_fail(self):
        """Test that a user cannot rate the same submission twice"""
        GrooveSubmissionRating.objects.create(
            groove_submission=self.submission,
            user_submitted=self.user,
            rating_value=self.rating_5
        )

        data = {
            "grooveSubmission": self.submission.id,
            "userSubmitted": self.user.id,
            "ratingValue": self.rating_3.id
        }
        response = self.client.post(
            "/groovesubmissionratings", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"],
                         "You already rated this submission!")

    def test_create_rating_on_inactive_weekly_groove_should_fail(self):
        """Test that a rating cannot be added to a submission from an inactive Weekly Groove"""
        inactive_groove = WeeklyGroove.objects.create(
            active=False,
            title="Old Groove",
            description="Past event",
            start_day="2025-02-01",
            end_day="2025-02-07"
        )
        old_submission = GrooveSubmission.objects.create(
            weekly_groove=inactive_groove,
            submitted_by=self.user,
            video_url="http://example.com/video-old.mp4",
            description="Old submission"
        )

        data = {
            "grooveSubmission": old_submission.id,
            "userSubmitted": self.user.id,
            "ratingValue": self.rating_5.id
        }
        response = self.client.post(
            "/groovesubmissionratings", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], "You can only rate submissions from the active Weekly Groove.")

    def test_update_groove_submission_rating(self):
        """Test updating a submission's rating (PUT /groovesubmissionratings/<id>)"""
        rating_entry = GrooveSubmissionRating.objects.create(
            groove_submission=self.submission,
            user_submitted=self.user,
            rating_value=self.rating_5
        )

        data = {
            "grooveSubmission": self.submission.id,
            "userSubmitted": self.user.id,
            "ratingValue": self.rating_3.id  # Changing rating from 5 to 3
        }
        response = self.client.put(
            f"/groovesubmissionratings/{rating_entry.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify update
        rating_entry.refresh_from_db()
        self.assertEqual(rating_entry.rating_value, self.rating_3)

    def test_delete_groove_submission_rating(self):
        """Test deleting a rating (DELETE /groovesubmissionratings/<id>)"""
        rating_entry = GrooveSubmissionRating.objects.create(
            groove_submission=self.submission,
            user_submitted=self.user,
            rating_value=self.rating_5
        )

        response = self.client.delete(
            f"/groovesubmissionratings/{rating_entry.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify deletion
        self.assertFalse(GrooveSubmissionRating.objects.filter(
            pk=rating_entry.id).exists())
