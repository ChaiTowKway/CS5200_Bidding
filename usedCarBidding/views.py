import datetime
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db import connection
import os

from .models import User

Car_ID = "JTDT4RCE7LJ025456"
currentUserId = "990"
currentUserName = "Lisa"
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



def car_detail (request):

    
    # print(type(Car_ID))    
    # sql1 = '''select * from Car where Car_ID = "JTDT4RCE7LJ025456"'''
    # print("********", sql0 == sql1)
    # print(sql0)
    # print(sql1)

    cursor = connection.cursor()
    sql0= '''select * from Car where Car_ID = "{Car_ID}";'''.format(Car_ID=Car_ID)
    cursor.execute(sql0)
    rows1 = cursor.fetchall()



    #Todo: what if no auction for this car ever--> max(Bidding_Price)
    cursor.execute('''select Auction_ID, max(Bidding_Price) from Bidding where Auction_ID = (select Auction_ID from Auction where Car_ID = '{Car_ID}');'''.format(Car_ID=Car_ID))
    rows2 = cursor.fetchall()


    auctionID_sql = '''select Auction_ID from Auction where Car_ID = '{Car_ID}';'''.format(Car_ID=Car_ID)
    cursor.execute(auctionID_sql)
    auctionID = cursor.fetchall()[0]
    print(auctionID, type(auctionID),"!!!!!!!!!!!!!!!!!")
    print(auctionID[0], type(auctionID[0]),"!!!!!!!!!!!!!!!!!")

    context = {
    "data1" : rows1,
    "data2" : rows2
    }




    return render(request, 'detail.html', context)



def place_bid(request):
    # auctionID = request.GET['auctionID']
    cursor = connection.cursor()
    check_winner_sql = '''select Winner_id from Auction where Car_ID = '{Car_ID}';'''.format(Car_ID=Car_ID)
    cursor.execute(check_winner_sql)
    check_winner = cursor.fetchall()[0][0]
    if check_winner != None:
        return HttpResponse("""Opps the auction for this car is over! You can not place a bid!!""")
    
    biddingPrice = request.GET['biddingPrice']
    bidder_ID = "2"


    
    

    auctionID_sql = '''select Auction_ID from Auction where Car_ID = '{Car_ID}';'''.format(Car_ID=Car_ID)
    cursor.execute(auctionID_sql)
    auctionID = cursor.fetchall()[0][0]

    sql = """INSERT INTO Bidding(Auction_ID, Bidder_ID, Bidding_Price) VALUES ({auctionID},{bidder_ID},{biddingPrice})""".format(bidder_ID=bidder_ID, biddingPrice=biddingPrice, auctionID=auctionID)

    
    cursor.execute(sql)



    return HttpResponse("""Congrats! You placed a bid!!""")




def car_detail_seller(request):

    
    # print(type(Car_ID))    
    # sql1 = '''select * from Car where Car_ID = "JTDT4RCE7LJ025456"'''
    # print("********", sql0 == sql1)
    # print(sql0)
    # print(sql1)

    cursor = connection.cursor()
    sql0= '''select * from Car where Car_ID = "{Car_ID}";'''.format(Car_ID=Car_ID)
    cursor.execute(sql0)
    rows1 = cursor.fetchall()



    #Todo: what if no auction for this car ever--> max(Bidding_Price)
    cursor.execute('''select * from Bidding where Auction_ID = (select Auction_ID from Auction where Car_ID = '{Car_ID}') order by Bidding_Price DESC;'''.format(Car_ID=Car_ID))
    rows2 = cursor.fetchall()

    context = {
    "data1" : rows1,
    "data2" : rows2
    }


    return render(request, 'detailSeller.html', context)


def end_bidding_for_seller(request):



    cursor = connection.cursor()
    auctionID_sql = '''select Auction_ID from Auction where Car_ID = '{Car_ID}';'''.format(Car_ID=Car_ID)
    cursor.execute(auctionID_sql)
    auctionID = cursor.fetchall()[0][0]
    print("@@@@@@@@@@@@@@1", auctionID)


    # Winner_id = 1 is a dummy id here just to mark this car has been sold
    set_winner_sql = '''update Auction set Winner_id = 1 where Auction_ID = {auctionID};'''.format(auctionID=auctionID)
    cursor.execute(set_winner_sql)

    set_car_status_sql = '''update Car set Current_Status = 'Sold' where Car_ID = '{Car_ID}';'''.format(Car_ID=Car_ID)
    cursor.execute(set_car_status_sql)
    
    
    
    
    return HttpResponse("""Congrats! You Car has been sold to the bidder with the highest bidder !!""")





def get_comments_for_auction(request):
    cursor = connection.cursor()
    auctionID_sql = '''select Auction_ID from Auction where Car_ID = '{Car_ID}';'''.format(Car_ID=Car_ID)
    cursor.execute(auctionID_sql)
    auctionID = cursor.fetchall()[0][0]

    get_comments_sql = '''select CommentID, create_by_user_Name, create_at, CommenContent from Comments where auction_id = {auctionID}'''.format(auctionID=auctionID)
    cursor.execute(get_comments_sql)
    rows1 = cursor.fetchall()
    print(type(rows1), rows1,"~~~~~~~")

    # map1 = {('John Doe', datetime.date(2023, 9, 1), 'This is a a nice car!!'):
    #         [('John Doe', datetime.date(2023, 9, 1), 'a!!'), ('John Doe', datetime.date(2023, 9, 1), 'b!!')]}

    comment_to_reply = {}
    for comment in rows1:
        CommentID = str(comment[0])
        reply_sql = '''select create_by_user_Name, create_at, ReplyContent from Reply where CommentID = {CommentID};'''.format(CommentID=CommentID)
        cursor.execute(reply_sql)
        rows2 = cursor.fetchall()
        comment_to_reply[comment] = rows2
    print(comment_to_reply)   

    context = {
    "data0" : rows1,
    # "data9" : map1
    "dataMap" : comment_to_reply
    }


    return render(request, 'comment.html', context)


def createComment(request):
    cursor = connection.cursor()
    auctionID_sql = '''select Auction_ID from Auction where Car_ID = '{Car_ID}';'''.format(Car_ID=Car_ID)
    cursor.execute(auctionID_sql)
    auctionID = cursor.fetchall()[0][0]
    print(auctionID, "&&&&&&&&&&&&1")

    commenContent = request.GET['commenContent']
    print(commenContent, "&&&&&&&&&&&&2")

    create_comment_sql = '''INSERT INTO Comments(CommenContent, create_at, create_by_user_ID, create_by_user_Name,auction_id) VALUES ('{commenContent}', CURRENT_DATE, {currentUserId}, '{currentUserName}', {auctionId});'''.format(commenContent=commenContent, currentUserId=currentUserId, currentUserName=currentUserName, auctionId=auctionID)
    print(create_comment_sql, "&&&&&&&&&&&&3")

    cursor.execute(create_comment_sql)

    return HttpResponse("""Congrats! You just post a comment!!""")


def createReply(request):
    cursor = connection.cursor()

    replyContent = request.GET['replyContent']
    commentId = request.GET['commentId']

    create_reply_sql = '''INSERT INTO Reply(ReplyContent,create_at, create_by_user_ID, create_by_user_Name, CommentID) VALUES ('{replyContent}', CURRENT_DATE, {currentUserId}, '{currentUserName}', {commentID});'''.format(replyContent=replyContent, currentUserId=currentUserId,currentUserName=currentUserName, commentID=commentId)
    cursor.execute(create_reply_sql)

    return HttpResponse("""Congrats! You just reply a comment!!""")