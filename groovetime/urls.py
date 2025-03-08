
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from groovetimeapi.views import (
    RatingView
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'ratings', RatingView, 'rating')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
