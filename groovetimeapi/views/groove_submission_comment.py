from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from groovetimeapi.models import (
    GrooveSubmissionComment,
    GrooveSubmission,
    GroovetimeUser
)

from datetime import datetime


class GrooveSubmissionCommentView(ViewSet):

    def retrieve(self, request, pk):

        try:

            single_groovetime_submission_comment = GrooveSubmissionComment.objects.get(
                pk=pk)
            serializer = GrooveSubmissionCommentSerializer(
                single_groovetime_submission_comment)
            return Response(serializer.data)

        except GrooveSubmissionComment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        groove_submission = request.query_params.get('groove_submission', None)
        commented_by = request.query_params.get('commented_by', None)

        all_groovetime_submission_comments = GrooveSubmissionComment.objects.all()

        if groove_submission is not None:
            all_groovetime_submission_comments = all_groovetime_submission_comments.filter(
                groove_submission=groove_submission)

        if commented_by is not None:
            all_groovetime_submission_comments = all_groovetime_submission_comments.filter(
                commented_by=commented_by)

        serializer = GrooveSubmissionCommentSerializer(
            all_groovetime_submission_comments, many=True)
        return Response(serializer.data)

    def create(self, request):

        groove_submission = GrooveSubmission.objects.get(
            pk=request.data["grooveSubmission"])
        commented_by = GroovetimeUser.objects.get(
            pk=request.data["commentedBy"])

        groove_submission_comment = GrooveSubmissionComment.objects.create(
            comment_text=request.data["commentText"],
            date_created=datetime,
            groove_submission=groove_submission,
            commented_by=commented_by
        )

        serializer = GrooveSubmissionCommentSerializer(
            groove_submission_comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        updated_groove_submission_comment = GrooveSubmissionComment.objects.get(
            pk=pk)
        updated_groove_submission_comment.comment_text = request.data["commentText"]

        updated_groove_submission_comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):

        deleted_groove_submission_comment = GrooveSubmissionComment.objects.get(
            pk=pk)
        deleted_groove_submission_comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GrooveSubmissionCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrooveSubmissionComment
        fields = (
            'groove_submission',
            'commented_by',
            'comment_text',
            'date_created',
        )
