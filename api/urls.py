from django.urls import path

from api.views import DataView, RandomView


urlpatterns = [
    path('', DataView.as_view(), name='index'),
    path('random', RandomView.as_view(), name='random'),
]
