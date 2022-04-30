import json
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from sqlapp.db_factory import db_factory
import logging

logging.basicConfig(filename="main.log", encoding='utf-8', level=logging.INFO)


# Create your views here.

class DefaultView(TemplateView):
    def get(self, request, **kwargs):
        context = {}
        return render(request, 'start_new.html', context=context)


@csrf_exempt
def index(request):
    return HttpResponse("Hello World!")

    # requests.post("https://localhost:3306/{function}", data={


# "server": "database-1.cyw17x3tauzw.us-east-1.rds.amazonaws.com",
# "user": "admin",
# "password": "password",
# "dbname": "testdb",
# "dbtype": "sqlserver",
# "tablename": "Persons"})
@csrf_exempt
def getInput(request):
    if request.method == 'POST':
        logging.info('Views :: Received POST request')
        config = json.loads(request.body)
        server_name = config['server']
        user = config['user']
        password = config['password']
        database_name = config['dbname']
        database_type = config['dbtype']
        tablename = config['tablename']
        db = db_factory.get_db(
            database_type,
            server_name=server_name,
            user=user,
            password=password,
            database=database_name,
            table = tablename
        )
        return db
    if request.method == 'GET':
        logging.info("Views :: Received GET request")
        server_name = request.GET['server']
        user = request.GET['user']
        password = request.GET['password']
        database_name = request.GET['dbname']
        database_type = request.GET['dbtype']
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
    # /testconnect
    try:
        db = getInput(request)
        logging.info("Views :: Successfully Connected to Database")
        return HttpResponse(json.dumps(
            {"status": "success", "message": "Connection is valid"}))
    except Exception as e:
        logging.error(f"Views :: {e}")
        return HttpResponse(json.dumps(
            {"status": "error", "message": "Check logs for error"}))


@csrf_exempt
def getTableMetadataList(request, **kwargs):
    # getmetadata/
    try:
        db = getInput(request)
        tbl_dict = db.get_table_metadata()
        logging.info(f"Views :: Metadata generated for {len(tbl_dict)} columns")
        return JsonResponse(tbl_dict, safe=False)
    except Exception as e:
        logging.error("Views :: Wrong request type")
        message = "Wrong request type"
        return HttpResponse(json.dumps(
            {"status": "error",
             "message": message}))


@csrf_exempt
def getDBList(request, **kwargs):
    # /listdbs
    try:
        db = getInput(request)
        db_dict = db.get_table_metadata()
        db_list = set([])
        for table_col in db_dict:
            db_list.add(table_col["table_cat"])
        set_db_list = list(db_list)
        logging.info(f"Views :: {len(set_db_list)} databases fetched successfully from database")
        return JsonResponse(set_db_list, safe=False)
    except Exception as e:
        logging.error(f"Views :: {e}")
        return HttpResponse(json.dumps(
            {"status": "error", "message": "Check logs for error"}))


@csrf_exempt
def getTableList(request, **kwargs):
    # /listtables
    try:
        db = getInput(request)
        tbl_dict = db.get_table_metadata()
        table_list = set([])
        for table_col in tbl_dict:
            table_list.add(table_col["table_name"])
        set_table_list = list(table_list)
        logging.info(f"Views :: {len(set_table_list)} tables fetched successfully from database")
        return JsonResponse(set_table_list, safe=False)
    except Exception as e:
        logging.error(f"Views :: {e}")
        return HttpResponse(json.dumps(
            {"status": "error", "message": "Check logs for error"}))


@csrf_exempt
def getColumnList(request, **kwargs):
    # listcolumns/
    if request.method == 'POST':
        config = json.loads(request.body)
        table_name = config['tablename']
    if request.method == 'GET':
        table_name = request.GET['tablename']
    logging.info(f"Views :: Fetching columns for table {table_name}")
    db = getInput(request)
    tbl_dict = db.get_table_metadata()
    set_table_list = []
    for metadata_columns in tbl_dict:
        if metadata_columns['table_name'] == table_name:
            set_table_list.append(metadata_columns['column_name'])
    logging.info(f"Views :: {len(set_table_list)} columns found for table {table_name}")
    return JsonResponse(set_table_list, safe=False)