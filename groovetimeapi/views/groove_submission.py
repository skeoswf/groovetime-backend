from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from groovetimeapi.models import (
    GrooveSubmission,
    WeeklyGroove,
    GroovetimeUser,
)

from .update_user_points import update_user_groove_points


class GrooveSubmissionView(ViewSet):

    def retrieve(self, request, pk):

        try:

            groove_submission = GrooveSubmission.objects.get(pk=pk)
            serializer = GrooveSubmissionSerializer(groove_submission)
            return Response(serializer.data)

        except GrooveSubmission.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        weekly_groove = request.query_params.get('weekly_groove', None)
        active = request.query_params.get("active", None)

        groove_submissions = GrooveSubmission.objects.all()

        if weekly_groove is not None:
            groove_submissions = groove_submissions.filter(
                weekly_groove=weekly_groove)

        if active is not None:
            groove_submissions = groove_submissions.filter(
                weekly_groove__active=True
            )

        serializer = GrooveSubmissionSerializer(groove_submissions, many=True)
        return Response(serializer.data)

    def create(self, request):

        weekly_groove = WeeklyGroove.objects.get(
            pk=request.data["weeklyGroove"])
        submitted_by = GroovetimeUser.objects.get(
            pk=request.data["submittedBy"])

        existing_submissions = GrooveSubmission.objects.filter(
            weekly_groove=weekly_groove,
            submitted_by=submitted_by
        ).count()

        # filters all the objects that have the same weekly groove and submitted by. eg. all the submissions made by the same user to the current groove.

        if existing_submissions >= 3:
            return Response(
                {"message": "You can only submit up to 3 videos per Weekly Groove."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # checks if there's 3 (or more), and then returns.

        groove_submission = GrooveSubmission.objects.create(
            video_url=request.data["videoURL"],
            description=request.data["description"],
            weekly_groove=weekly_groove,
            submitted_by=submitted_by
        )

        update_user_groove_points(submitted_by)
        serializer = GrooveSubmissionSerializer(groove_submission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        groove_submission = GrooveSubmission.objects.get(pk=pk)
        groove_submission.description = request.data["description"]

        groove_submission.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):

        groove_submission = GrooveSubmission.objects.get(pk=pk)
        groove_submission.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GrooveSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrooveSubmission
        fields = (
            'weekly_groove',
            'submitted_by',
            'video_url',
            'description',
            'average_rating',
            'user_ratings'
        )
