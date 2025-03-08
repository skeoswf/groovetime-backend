from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from groovetimeapi.models import WeeklyGroove


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
            weekly_grooves = weekly_grooves.filter(active=active)

        serializer = WeeklyGrooveSerializer(weekly_grooves, many=True)
        return Response(serializer.data)

    def create(self, request):
        WeeklyGroove.objects.filter(active=True).update(active=False)

        weekly_groove = WeeklyGroove.objects.create(
            active=request.data["active"],
            title=request.data["title"],
            description=request.data["description"],
            start_day=request.data["startDay"],
            end_day=request.data["endDay"]
        )

        serializer = WeeklyGrooveSerializer(weekly_groove)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

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
