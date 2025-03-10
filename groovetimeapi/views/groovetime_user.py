from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from groovetimeapi.models import (
    GrooveSubmission,
    GroovetimeUser
)

from datetime import datetime


class GroovetimeUserView(ViewSet):

    def retrieve(self, request, pk):

        try:

            single_groovetime_user = GroovetimeUser.objects.get(pk=pk)
            serializer = GroovetimeUserSerializer(single_groovetime_user)
            return Response(serializer.data)

        except GroovetimeUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        admin = request.query_params.get('admin', None)

        all_groovetime_users = GroovetimeUser.objects.all()

        if admin is not None:
            all_groovetime_users = all_groovetime_users.filter(
                admin=admin)

        serializer = GroovetimeUserSerializer(all_groovetime_users, many=True)
        return Response(serializer.data)

    def create(self, request):

        created_groovetime_user = GroovetimeUser.objects.create(
            uid=request.data["uid"],
            profile_picture=request.data["profilePicture"],
            bio=request.data["bio"],

            date_joined=datetime
        )

        serializer = GroovetimeUserSerializer(created_groovetime_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        updated_groovetime_user = GroovetimeUser.objects.get(pk=pk)
        updated_groovetime_user.profile_picture = request.data["profilePicture"]
        updated_groovetime_user.bio = request.data["bio"]

        updated_groovetime_user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):

        deleted_groovetime_user = GroovetimeUser.objects.get(pk=pk)
        deleted_groovetime_user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GroovetimeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroovetimeUser
        fields = (
            'uid',
            'profile_picture',
            'bio',
            'groove_points',
            'grooves_won',
            'date_joined',
            'admin'
        )
