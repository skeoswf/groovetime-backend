from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from groovetimeapi.models import (
    WeeklyGroove,
    GrooveSubmission,
    GroovetimeUser
)

from .update_user_points import update_user_groove_points


class WeeklyGrooveView(ViewSet):

    def retrieve(self, request, pk):

        try:

            weekly_groove = WeeklyGroove.objects.get(pk=pk)
            serializer = WeeklyGrooveSerializer(weekly_groove)
            return Response(serializer.data)

        except WeeklyGroove.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        active = request.query_params.get('active', None)

        weekly_grooves = WeeklyGroove.objects.all()

        if active is not None:
            active = active.lower() == "true"
            weekly_grooves = weekly_grooves.filter(active=active)

        serializer = WeeklyGrooveSerializer(weekly_grooves, many=True)
        return Response(serializer.data)

    def create(self, request):
        previous_weekly_groove = WeeklyGroove.objects.filter(
            active=True).first()
        # capture previous weekly groove to find winner
        WeeklyGroove.objects.filter(active=True).update(active=False)

        if previous_weekly_groove:
            highest_submission = GrooveSubmission.objects.filter(
                weekly_groove=previous_weekly_groove
            ).order_by('-average_rating').first()

            if highest_submission:
                winner = highest_submission.submitted_by
                winner.grooves_won += 1
                winner.save()

        weekly_groove = WeeklyGroove.objects.create(
            active=request.data["active"],
            title=request.data["title"],
            description=request.data["description"],
            start_day=request.data["startDay"],
            end_day=request.data["endDay"]
        )

        all_users = GroovetimeUser.objects.all()
        for user in all_users:
            update_user_groove_points(user)

        serializer = WeeklyGrooveSerializer(weekly_groove)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        try:
            weekly_groove = WeeklyGroove.objects.get(pk=pk)
        except WeeklyGroove.DoesNotExist:
            return Response({"message": "Weekly Groove not found."}, status=status.HTTP_404_NOT_FOUND)

        weekly_groove = WeeklyGroove.objects.get(pk=pk)
        weekly_groove.active = request.data["active"]
        weekly_groove.title = request.data["title"]
        weekly_groove.description = request.data["description"]
        weekly_groove.start_day = request.data["startDay"]
        weekly_groove.end_day = request.data["endDay"]

        weekly_groove.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):

        weekly_groove = WeeklyGroove.objects.get(pk=pk)
        weekly_groove.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class WeeklyGrooveSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeeklyGroove
        fields = (
            'active',
            'title',
            'description',
            'start_day',
            'end_day'
        )
