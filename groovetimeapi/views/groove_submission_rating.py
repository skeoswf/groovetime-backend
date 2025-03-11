from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from groovetimeapi.models import (
    GroovetimeUser,
    GrooveSubmission,
    Rating,
    GrooveSubmissionRating,
)

from .update_user_points import update_user_groove_points


class GrooveSubmissionRatingView(ViewSet):

    def retrieve(self, request, pk):
        single_submission_rating = GrooveSubmissionRating.objects.get(pk=pk)
        serializer = GrooveSubmissionRatingSerializer(
            single_submission_rating)
        return Response(serializer.data)

    def list(self, request):
        groove_submission = request.query_params.get('groove_submission', None)

        all_submission_ratings = GrooveSubmissionRating.objects.all()

        if groove_submission is not None:
            all_submission_ratings = all_submission_ratings.filter(
                groove_submission=groove_submission)

        # show ratings attached to a particular submission

        serializer = GrooveSubmissionRatingSerializer(
            all_submission_ratings, many=True)
        return Response(serializer.data)

    def create(self, request):

        groove_submission = GrooveSubmission.objects.get(
            pk=request.data["grooveSubmission"])
        user_submitted = GroovetimeUser.objects.get(
            pk=request.data["userSubmitted"])
        rating_value = Rating.objects.get(pk=request.data["ratingValue"])

        if not groove_submission.weekly_groove.active:
            return Response(
                {"message": "You can only rate submissions from the active Weekly Groove."},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_rating = GrooveSubmissionRating.objects.filter(
            groove_submission=groove_submission,
            user_submitted=user_submitted
        ).count()

        if existing_rating >= 1:
            return Response(
                {"message": "You already rated this submission!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        groove_submission_rating = GrooveSubmissionRating.objects.create(
            groove_submission=groove_submission,
            user_submitted=user_submitted,
            rating_value=rating_value
        )

        groove_submission.user_ratings.add(rating_value)
        all_ratings = groove_submission.user_ratings.values_list(
            'value', flat=True)

        groove_submission.average_rating = sum(
            all_ratings) / len(all_ratings) if all_ratings else None

        groove_submission.save()
        update_user_groove_points(groove_submission.submitted_by)

        serializer = GrooveSubmissionRatingSerializer(groove_submission_rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        groove_submission_rating = GrooveSubmissionRating.objects.get(pk=pk)

        groove_submission = GrooveSubmission.objects.get(
            pk=request.data["grooveSubmission"])
        user_submitted = GroovetimeUser.objects.get(
            pk=request.data["userSubmitted"])
        rating_value = Rating.objects.get(pk=request.data["ratingValue"])

        groove_submission_rating.groove_submission = groove_submission
        groove_submission_rating.user_submitted = user_submitted
        groove_submission_rating.rating_value = rating_value

        groove_submission_rating.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        groove_submission_rating = GrooveSubmissionRating.objects.get(pk=pk)
        groove_submission_rating.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GrooveSubmissionRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrooveSubmissionRating
        fields = (
            'groove_submission',
            'user_submitted',
            'rating_value'
        )
