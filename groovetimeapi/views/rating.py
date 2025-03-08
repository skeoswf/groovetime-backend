from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from groovetimeapi.models import Rating


class RatingView(ViewSet):

    def retrieve(self, request, pk):

        try:
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating)
            return Response(serializer.data)

        except Rating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = (
            'id',
            'value',
            'description'
        )
