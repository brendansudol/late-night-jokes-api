from django.urls import path

from api.views import DataView


urlpatterns = [
    path('', DataView.as_view(), name='index'),
]
