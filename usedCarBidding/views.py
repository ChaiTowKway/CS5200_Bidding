from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db import connection



def index(request):
    return HttpResponse("Hello, world. You're at the bidding index.")

from django.http import HttpResponse
from django.db import connection
import os

def check_db_connection(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SHOW TABLES;')
            tables = cursor.fetchall()
            cursor.execute('SELECT DATABASE(), @@version, @@version_comment, @@version_compile_os, @@character_set_server;')
            database_name, version, version_comment, compile_os, character_set = cursor.fetchone()
        
        response_content = "<h2>Database Details:</h2>"
        response_content += f"<strong>Database Name:</strong> {database_name}<br>"
        response_content += f"<strong>MySQL Version:</strong> {version}<br>"
        response_content += f"<strong>Version Comment:</strong> {version_comment}<br>"
        response_content += f"<strong>Compile OS:</strong> {compile_os}<br>"
        response_content += f"<strong>Character Set:</strong> {character_set}<br>"
        
        response_content += "<h2>Tables in the Database:</h2>"
        for table in tables:
            response_content += f"<strong>{table[0]}</strong><br>"
        
        return HttpResponse(response_content)
    except Exception as e:
        return HttpResponse(f"Database connection failed: {str(e)}")

    

    