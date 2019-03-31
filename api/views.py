from django.http import JsonResponse
from django.views.generic import View

from api.models import Joke


class DataView(View):
    model = Joke
    limit = 100

    def get(self, request, *args, **kwargs):
        queryset = self.model.objects.search(request.GET)
        results = [entry.to_dict() for entry in queryset[:self.limit]]
        return JsonResponse({'results': results})
