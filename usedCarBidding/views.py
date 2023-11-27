from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db import connection
import os, json
from .models import User
import openai
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.db import connection

# Set up your OpenAI API key
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

def testmysql(request):
    user = User.objects.all()
    context = {
        'user_id': user[0].userid,
        'user_name': user[0].name,
        'user_email': user[0].email,
    }
    return render(request, 'home.html', context)

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

def chat(request):
    return render(request, 'chatbot/chat.html')

def respond(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        def get_all_attributes():
            models = dict()
            for app_config in apps.get_app_configs():
                # Iterate over all models in each app
                for model in app_config.get_models():
                    # Get the model's fields
                    models[model.__name__] = list()
                    fields = model._meta.get_fields()
                    attribute_names = [field.name for field in fields]
                    models[model.__name__].extend(attribute_names)

            return models
        
        # Usage
        all_attributes = get_all_attributes()
        db_tables = f"The backend database has these tables: {all_attributes}"
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{db_tables}. Translate the following human query into a SQL query:\n\n{user_input}\n\nSQL Query:",
                }
            ],
            model="gpt-3.5-turbo",
        )

        # Extract the assistant's reply from the OpenAI API response
        assistant_message = response.choices[0].message.content
        print(assistant_message)
        query_result = connect_db(assistant_message)
        query_result = str(query_result)
        print(query_result)
        query_result_rephase = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"The question from user is {user_input}. Rephase to this response to human languange:\n\n{query_result}\n\n",
                }
            ],
            model="gpt-3.5-turbo",
        )
        # Prepare the response data
        response_data = {'message': query_result_rephase.choices[0].message.content}
        return JsonResponse(response_data)

    # If the request method is not POST, return an empty response
    return JsonResponse({})

def connect_db(query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        response = cursor.fetchall()
        if "UPDATE" in query:
            return "Update successfully"
        else:
            columns1 = [col[0] for col in cursor.description]
            results1 = [dict(zip(columns1, row)) for row in response]
            return results1
    except:
        return "I apologize, but I'm unable to find a solution for your query. Could you please rephrase your question or provide more details so that I can better assist you?"
