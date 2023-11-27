from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db import connection
import os

from .models import User

Car_ID = "4T1F11AK5PU731597"
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
