from django.http import HttpResponse
from rest_framework.generics import GenericAPIView


class Smoke(GenericAPIView):
    def get(self, request):
        return HttpResponse({"msg": "OK"})
