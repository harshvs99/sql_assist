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
def getInput(request):
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
        return db


@csrf_exempt
def connectDatabase(request, **kwargs):
    # if request.method == 'GET':
    #
    try:
        db = getInput(request)
        print("this is db: ", db)
        return JsonResponse(request, safe=False)
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps(
            {"status": "error", "message": "Check logs for error"}))


@csrf_exempt
def getTableList(request, **kwargs):
    try:
        db = getInput(request)
        tbl_dict = db.get_table_metadata()
        table_list = set([])
        for table_col in tbl_dict:
            table_list.add(table_col["table_cat"])
        set_table_list = list(table_list)
        return JsonResponse(set_table_list, safe=False)
    except Exception as e:
        message = ""
        if request.method == 'GET':
            print("Only POST requests accepted")
            message = "Only POST requests accepted"
        else:
            print("Wrong request type")
            message = "Wrong request type"
        return HttpResponse(json.dumps(
            {"status": "error", "message": "Check logs for error"}))


@csrf_exempt
def getTableMetadataList(request, **kwargs):
    message = ""
    try:
        db = getInput(request)
        tbl_dict = db.get_table_metadata()
        print("Table list generated")
        return JsonResponse(tbl_dict, safe=False)
    except Exception as e:
        if request.method == 'GET':
            print("Only POST requests accepted")
            message = "Only POST requests accepted"
        else:
            print("Wrong request type")
            message = "Wrong request type"
        return HttpResponse(json.dumps(
            {"status": "error",
             "message": message},
            content_type="application/json"))


@csrf_exempt
def getColumnList(request, **kwargs):
    if request.method == 'POST':
        config = json.loads(request.body)
        table_name = config['tablename']
    db = getInput(request)
    tbl_dict = db.get_table_metadata()
    set_table_list = []
    print("tbl: ", tbl_dict)
    for metadata_columns in tbl_dict:
        if metadata_columns['table_name'] == table_name:
            set_table_list.append(metadata_columns['column_name'])
    return JsonResponse(set_table_list, safe=False)
