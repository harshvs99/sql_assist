import json
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


# from sqlapp.models import Jobs


# Create your views here.

# class DefaultView(TemplateView):
#     def get(self, request, **kwargs):
#         context = {}
#         return render(request, 'start_new.html', context=context)


@csrf_exempt
def index(request):
    return HttpResponse("Hello World!")


@csrf_exempt
def connectDatabase(request, **kwargs):
    # if request.method == 'GET':
    #
    if request.method == 'POST':
        config = json.loads(request.body)
        server_name = config['server']
        # db_dict = {config, server_name}
        print(server_name)
        return JsonResponse(config, safe=False)
