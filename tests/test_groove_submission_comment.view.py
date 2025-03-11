from rest_framework import status
from rest_framework.test import APITestCase
from groovetimeapi.models import WeeklyGroove, GrooveSubmission, GroovetimeUser, GrooveSubmissionComment


class GrooveSubmissionCommentTests(APITestCase):

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
        cls.comment = GrooveSubmissionComment.objects.create(
            groove_submission=cls.submission,
            commented_by=cls.user,
            comment_text="This is a test comment"
        )

    def test_list_groove_submission_comments(self):
        """Test retrieving all groove submission comments (GET /groovesubmissioncomments)"""
        response = self.client.get("/groovesubmissioncomments")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_comments_by_submission(self):
        """Test retrieving comments for a specific submission (GET /groovesubmissioncomments?groove_submission=<id>)"""
        response = self.client.get(
            f"/groovesubmissioncomments?groove_submission={self.submission.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_comments_by_user(self):
        """Test retrieving comments made by a specific user (GET /groovesubmissioncomments?commented_by=<id>)"""
        response = self.client.get(
            f"/groovesubmissioncomments?commented_by={self.user.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_single_comment(self):
        """Test retrieving a single comment by ID (GET /groovesubmissioncomments/<id>)"""
        response = self.client.get(
            f"/groovesubmissioncomments/{self.comment.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["comment_text"], self.comment.comment_text)

    def test_retrieve_nonexistent_comment(self):
        """Test retrieving a non-existent comment should return 404"""
        response = self.client.get(
            "/groovesubmissioncomments/999")  # Assuming 999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment(self):
        """Test creating a new groove submission comment (POST /groovesubmissioncomments)"""
        data = {
            "grooveSubmission": self.submission.id,
            "commentedBy": self.user.id,
            "commentText": "Another test comment"
        }
        response = self.client.post(
            "/groovesubmissioncomments", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["comment_text"], "Another test comment")

    def test_update_comment(self):
        """Test updating a comment's text (PUT /groovesubmissioncomments/<id>)"""
        data = {"commentText": "Updated comment"}
        response = self.client.put(
            f"/groovesubmissioncomments/{self.comment.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify update
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.comment_text, "Updated comment")

    def test_update_nonexistent_comment(self):
        """Test updating a non-existent comment should return 404"""
        data = {"commentText": "Shouldn't work"}
        response = self.client.put(
            "/groovesubmissioncomments/999", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment(self):
        """Test deleting a comment (DELETE /groovesubmissioncomments/<id>)"""
        response = self.client.delete(
            f"/groovesubmissioncomments/{self.comment.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify deletion
        self.assertFalse(GrooveSubmissionComment.objects.filter(
            pk=self.comment.id).exists())

    def test_delete_nonexistent_comment(self):
        """Test deleting a non-existent comment should return 404"""
        response = self.client.delete("/groovesubmissioncomments/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
