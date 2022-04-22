import json
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from sqlapp.db_factory import db_factory


# from sqlapp.models import Jobs


# Create your views here.

class DefaultView(TemplateView):
    def get(self, request, **kwargs):
        context = {}
        return render(request, 'start_new.html', context=context)


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
        user = config['user']
        password = config['password']
        database_name = config['dbname']
        database_type = config['dbtype']
        db = db_factory.get_db(
            database_type,
            server_name=server_name,
            user=user,
            password=password,
            database=database_name
        )
        # list_db = db.get_database_list()
        # list_tables = db.get_table_list()
        print("this is db: ", db)
        return JsonResponse(config, safe=False)


@csrf_exempt
def get_table_list(request, **kwargs):
    if request.method == 'POST':
        config = json.loads(request.body)
        server_name = config['server']
        user = config['user']
        password = config['password']
        database_name = config['dbname']
        database_type = config['dbtype']
        db = db_factory.get_db(
            database_type,
            server_name=server_name,
            user=user,
            password=password,
            database=database_name
        )
        tbl_dict = db.get_table_list()
        return JsonResponse(tbl_dict, safe=False)

