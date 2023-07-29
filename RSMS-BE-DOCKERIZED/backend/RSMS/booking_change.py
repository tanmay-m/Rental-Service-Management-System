import psycopg2
import time
from datetime import datetime

import urllib.parse
result = urllib.parse.urlparse("postgres://lzyrqsdcgabpoz:c39a04940d1d77be940e7fff2f62fa9b15cf57dc120d5948951ddc1aaf198b80@ec2-34-197-91-131.compute-1.amazonaws.com:5432/d98pi1ptri5f7m")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

timeAt = datetime.now().date()

while True:
    connection = psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname,
        port = port
    )
    cursor = connection.cursor()
    cursor.execute("select id from api_rent_items where rent_status != 'PENDING'")
    rent_items = cursor.fetchall()
    item_and_status = []
    d = {}
    for rent_item in rent_items:
        query = f'select from_date, to_date from api_orders where rent_id = \'{rent_item[0]}\''
        cursor.execute(query)
        status = "AVAILABLE"
        try:
            orders = cursor.fetchall()
            d[rent_item[0]] = orders
        except Exception as e:
            print("no orders found for ", rent_item[0])
            d[rent_item[0]] = []

    for ri, ro in d.items():
        cov = False
        for o in ro:
            if o[0] <= timeAt and o[1] <= timeAt:
                cov = True
                break
        item_and_status.append((ri, cov))
    for items in item_and_status:
        status = "AVAILABLE"
        if items[1]:
            status = "BOOKED"
        q = f'update api_rent_items  set rent_status=\'{status}\' where id=\'{items[0]}\''
        print("qq = ", q)
        cursor.execute(q)
    connection.commit()
    time.sleep(1)