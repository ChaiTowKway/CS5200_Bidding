import datetime
from django.contrib.auth import authenticate, login
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from openai import OpenAI
import openai
from .models import User
import json
import os
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
import datetime
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from openai import OpenAI
import openai
from .models import User
import json
import os
from django.db import connection
from django.http import HttpResponse


# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             messages.success(request, f'Account created for {email}!')
#             # Redirect to login page after registration
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'registration/register.html', {'form': form})


# Create your views here.

# Set up your OpenAI API key
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)


Car_ID = "JTDT4RCE7LJ025456"
currentUserId = "990"
currentUserName = "Lisa"


def testmysql(request):
    if request.user.is_authenticated:
        context = {
            'user_id': request.user.userid,
            'user_name': request.user.name,
            'user_email': request.user.email,
            'is_authenticated': True,
        }
    else:
        context = {
            'user_id': 'N/A',
            'user_name': 'Guest',
            'user_email': 'N/A',
            'is_authenticated': False,
        }

    return render(request, 'home.html', context)


def check_db_connection(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SHOW TABLES;')
            tables = cursor.fetchall()
            cursor.execute(
                'SELECT DATABASE(), @@version, @@version_comment, @@version_compile_os, @@character_set_server;')
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
        query_result = connect_db(assistant_message, request)
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
        response_data = {
            'message': query_result_rephase.choices[0].message.content}
        return JsonResponse(response_data)

    # If the request method is not POST, return an empty response
    return JsonResponse({})


def connect_db(query, request):
    cursor = connection.cursor()
    try:
        if "DELETE" in query:
            if not request.user.isadmin:
                return "Sorry, only admin can perform the delete action."
        cursor.execute(query)
        response = cursor.fetchall()
        if "UPDATE" in query:
            return "Update successfully"
        elif "DELETE" in query:
            if request.user.isadmin:
                return "Successfully removed"
        else:
            columns1 = [col[0] for col in cursor.description]
            results1 = [dict(zip(columns1, row)) for row in response]
            return results1
    except:
        return "I apologize, but I'm unable to find a solution for your query. Could you please rephrase your question or provide more details so that I can better assist you?"

def car_list(request):
        cursor = connection.cursor()
        # sql0 = '''select * from Car where Car_ID = "{Car_ID}";'''.format(Car_ID=Car_ID)
        sql = '''select * from Car ;'''  # where current_status='For Sale'
        cursor.execute(sql)
        rows = list(cursor.fetchall())

        title = [title[0] for title in cursor.description]
        res = []
        for item in rows:
            res.append(dict(list(zip(title, item))))

        # print(res)
        context = {
            "carData": res,
        }

        return render(request, 'index.html', context)


def car_detail(request):

    # print(type(Car_ID))
    # sql1 = '''select * from Car where Car_ID = "JTDT4RCE7LJ025456"'''
    # print("********", sql0 == sql1)
    # print(sql0)
    # print(sql1)
    Car_id = request.GET['carId']
    cursor = connection.cursor()
    sql0 = '''select * from Car where Car_ID = "{Car_ID}";'''.format(Car_ID=Car_id)
    cursor.execute(sql0)
    rows1 = cursor.fetchall()

    cursor = connection.cursor()
    sql0 = '''select * from Car where Car_ID = "{Car_ID}";'''.format(
        Car_ID=Car_ID)
    cursor.execute(sql0)
    rows1 = cursor.fetchall()

    # Todo: what if no auction for this car ever--> max(Bidding_Price)
    cursor.execute(
        '''select Auction_ID, max(Bidding_Price) as Bidding_Price from Bidding where Auction_ID = (select Auction_ID from Auction where Car_ID = '{Car_ID}') group by Auction_ID,Bidding_Price ;'''.format(
            Car_ID=Car_ID))

    rows2 = cursor.fetchall()
    print(rows2)

    auctionID_sql = '''select Auction_ID from Auction where Car_ID = '{Car_ID}';'''.format(Car_ID=Car_ID)
    cursor.execute(auctionID_sql)
    # auctionID = cursor.fetchall()[0]

    auctionID = cursor.fetchall()
    print(auctionID)
    if len(auctionID) == 0:
        # if auctionID is None:
        print('无数据')
    else:
        auctionID = auctionID[0]
        print(auctionID, type(auctionID), "!!!!!!!!!!!!!!!!!")
        print(auctionID[0], type(auctionID[0]), "!!!!!!!!!!!!!!!!!")

    context = {
        "data1": rows1,
        "data2": rows2
    }

    return render(request, 'detail.html', context)


def place_bid(request):
    # auctionID = request.GET['auctionID']
    cursor = connection.cursor()
    check_winner_sql = '''select Winner_id from Auction where Car_ID = '{Car_ID}';'''.format(
        Car_ID=Car_ID)
    cursor.execute(check_winner_sql)
    check_winner = cursor.fetchall()[0][0]
    if check_winner != None:
        return HttpResponse("""Opps the auction for this car is over! You can not place a bid!!""")

    biddingPrice = request.GET['biddingPrice']
    bidder_ID = "2"

    auctionID_sql = '''select Auction_ID from Auction where Car_ID = '{Car_ID}';'''.format(
        Car_ID=Car_ID)
    cursor.execute(auctionID_sql)
    auctionID = cursor.fetchall()[0][0]

    sql = """INSERT INTO Bidding(Auction_ID, Bidder_ID, Bidding_Price) VALUES ({auctionID},{bidder_ID},{biddingPrice})""".format(
        bidder_ID=bidder_ID, biddingPrice=biddingPrice, auctionID=auctionID)

    cursor.execute(sql)

    return HttpResponse("""Congrats! You placed a bid!!""")


def car_detail_seller(request):

    # print(type(Car_ID))
    # sql1 = '''select * from Car where Car_ID = "JTDT4RCE7LJ025456"'''
    # print("********", sql0 == sql1)
    # print(sql0)
    # print(sql1)

    cursor = connection.cursor()
    sql0 = '''select * from Car where Car_ID = "{Car_ID}";'''.format(
        Car_ID=Car_ID)
    cursor.execute(sql0)
    rows1 = cursor.fetchall()

    # Todo: what if no auction for this car ever--> max(Bidding_Price)
    cursor.execute(
        '''select * from Bidding where Auction_ID = (select Auction_ID from Auction where Car_ID = '{Car_ID}') order by Bidding_Price DESC;'''.format(Car_ID=Car_ID))
    rows2 = cursor.fetchall()

    context = {
        "data1": rows1,
        "data2": rows2
    }

    return render(request, 'detailSeller.html', context)


def end_bidding_for_seller(request):

    cursor = connection.cursor()
    auctionID_sql = '''select Auction_ID from Auction where Car_ID = '{Car_ID}';'''.format(
        Car_ID=Car_ID)
    cursor.execute(auctionID_sql)
    auctionID = cursor.fetchall()[0][0]
    print("@@@@@@@@@@@@@@1", auctionID)

    # Winner_id = 1 is a dummy id here just to mark this car has been sold
    set_winner_sql = '''update Auction set Winner_id = 1 where Auction_ID = {auctionID};'''.format(
        auctionID=auctionID)
    cursor.execute(set_winner_sql)

    set_car_status_sql = '''update Car set Current_Status = 'Sold' where Car_ID = '{Car_ID}';'''.format(
        Car_ID=Car_ID)
    cursor.execute(set_car_status_sql)

    return HttpResponse("""Congrats! You Car has been sold to the bidder with the highest bidder !!""")


def get_comments_for_auction(request):
    cursor = connection.cursor()
    auctionID_sql = '''select Auction_ID from Auction where Car_ID = '{Car_ID}';'''.format(
        Car_ID=Car_ID)
    cursor.execute(auctionID_sql)
    auctionID = cursor.fetchall()[0][0]

    get_comments_sql = '''select CommentID, create_by_user_Name, create_at, CommenContent from Comments where auction_id = {auctionID}'''.format(
        auctionID=auctionID)
    cursor.execute(get_comments_sql)
    rows1 = cursor.fetchall()
    print(type(rows1), rows1, "~~~~~~~")

    # map1 = {('John Doe', datetime.date(2023, 9, 1), 'This is a a nice car!!'):
    #         [('John Doe', datetime.date(2023, 9, 1), 'a!!'), ('John Doe', datetime.date(2023, 9, 1), 'b!!')]}

    comment_to_reply = {}
    for comment in rows1:
        CommentID = str(comment[0])
        reply_sql = '''select create_by_user_Name, create_at, ReplyContent from Reply where CommentID = {CommentID};'''.format(
            CommentID=CommentID)
        cursor.execute(reply_sql)
        rows2 = cursor.fetchall()
        comment_to_reply[comment] = rows2
    print(comment_to_reply)

    context = {
        "data0": rows1,
        # "data9" : map1
        "dataMap": comment_to_reply
    }

    return render(request, 'comment.html', context)


def createComment(request):
    cursor = connection.cursor()
    auctionID_sql = '''select Auction_ID from Auction where Car_ID = '{Car_ID}';'''.format(
        Car_ID=Car_ID)
    cursor.execute(auctionID_sql)
    auctionID = cursor.fetchall()[0][0]
    print(auctionID, "&&&&&&&&&&&&1")

    commenContent = request.GET['commenContent']
    print(commenContent, "&&&&&&&&&&&&2")

    create_comment_sql = '''INSERT INTO Comments(CommenContent, create_at, create_by_user_ID, create_by_user_Name,auction_id) VALUES ('{commenContent}', CURRENT_DATE, {currentUserId}, '{currentUserName}', {auctionId});'''.format(
        commenContent=commenContent, currentUserId=currentUserId, currentUserName=currentUserName, auctionId=auctionID)
    print(create_comment_sql, "&&&&&&&&&&&&3")

    cursor.execute(create_comment_sql)

    return HttpResponse("""Congrats! You just post a comment!!""")


def createReply(request):
    cursor = connection.cursor()

    replyContent = request.GET['replyContent']
    commentId = request.GET['commentId']

    create_reply_sql = '''INSERT INTO Reply(ReplyContent,create_at, create_by_user_ID, create_by_user_Name, CommentID) VALUES ('{replyContent}', CURRENT_DATE, {currentUserId}, '{currentUserName}', {commentID});'''.format(
        replyContent=replyContent, currentUserId=currentUserId, currentUserName=currentUserName, commentID=commentId)
    cursor.execute(create_reply_sql)

    return HttpResponse("""Congrats! You just reply a comment!!""")


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Replace 'login_url' with your login URL name
            return redirect('login_url')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
