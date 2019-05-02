from django.http import JsonResponse
from django.views.generic import View

from api.models import Joke


class DataView(View):
    model = Joke
    limit = 500

    def get(self, request, *args, **kwargs):
        params = request.GET
        return JsonResponse({'results': self.fetch_data(params)})

    def fetch_data(self, params):
        # return nothing if query less than 3 characters
        query = params.get('query')
        if not query or len(query) < 3:
            return []

        queryset = self.model.objects.search(params)
        return [entry.to_dict() for entry in queryset[:self.limit]]


class RandomView(View):
    model = Joke
    limit = 100

    def get(self, request, *args, **kwargs):
        results = self.model.objects.rand(self.limit)
        return JsonResponse({'results': results})
