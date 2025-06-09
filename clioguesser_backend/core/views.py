from django.shortcuts import render
from django.http import JsonResponse
from .models import Cliopatria

def cliopatria_list(request):
    cliopatria_objects = Cliopatria.objects.all().values()
    return JsonResponse(list(cliopatria_objects), safe=False)

def cliopatria_detail(request, pk):
    try:
        cliopatria_object = Cliopatria.objects.get(pk=pk)
        return JsonResponse(cliopatria_object)
    except Cliopatria.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)