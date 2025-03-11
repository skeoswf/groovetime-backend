
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from groovetimeapi.views import (
    RatingView,
    WeeklyGrooveView,
    GrooveSubmissionView,
    GroovetimeUserView,
    GrooveSubmissionRatingView,
    GrooveSubmissionCommentView
)

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'ratings', RatingView, 'rating')


router.register(
    r'weeklygrooves',
    WeeklyGrooveView,
    'weeklygroove'
)

router.register(
    r'groovesubmissions',
    GrooveSubmissionView,
    'groovesubmission'
)

router.register(
    r'groovetimeusers',
    GroovetimeUserView,
    'groovetimeuser'
)

router.register(
    r'groovesubmissionratings',
    GrooveSubmissionRatingView,
    'groovesubmissionrating'
)

router.register(
    r'groovesubmissioncomments',
    GrooveSubmissionCommentView,
    'groovesubmissioncomment'
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
