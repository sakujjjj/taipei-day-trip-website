from flask import Flask
from flask import jsonify
import mysql.connector
import json

with open("C:\\Users\\user\\taipei-day-trip-website\\data\\taipei-attractions.json",'r',encoding="utf-8") as f:
    json_obj = json.load(f)

# print(json_obj)
# print(type(json_obj))

#讀字串轉dict
# json_data = open("taipei-attractions.json",encoding="utf-8").read()
# # print(json_data)
# # print(type(json_data))
# json_obj=json.loads(json_data)
# print(json_obj)
# print(type(json_obj))

#
# data = json.load(open("taipei-attractions.json",encoding="utf-8"))
# print(data)
# print(type(data))




con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="website"
)
cursor=con.cursor()
# images=[]
for item in json_obj['result']['results']:
    # print(item)
    # name=item.get("stitle")
    name=item["stitle"]
    print(name)
    category=item.get("CAT2")
    description=item.get("xbody")
    description=description.split("。")[0]+"。"
    address=item.get("address")
    transport=item.get("info")
    
    mrt=item.get("MRT")
    latitude=item.get("latitude")
    longitude=item.get("longitude")
    
    # images=item.get("file")
    # images=images.split("https://")
    # images=item.get("file").split("https://")
    # images=item["file"].split("https://")
    # print(images)
    
    images=[]
    for i in item["file"].split("https://"):
        if i.lower().endswith("jpg") :
            #  image = i
            #  print(image)
            images.append("https://"+i)
            # print(name)
            # print(images)
            # cursor.executemany("INSERT INTO travel (images) VALUES (%s)", (images))
            # for x in images:
            #     cursor.execute(sql, x)
    print(images)
    print(type(images))

# print(images)
# print(type(images))

    # print(name, category, description, address, transport, mrt, latitude, longitude, images)
    # print(type(images))
    # cursor.execute("insert into travel (name, category, description, address, transport, mrt, latitude, longitude, images) value(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, category, description, address, transport, mrt, latitude, longitude, images))
    
    # cursor.execute("insert into travel (name, category, description, address, transport, mrt, latitude, longitude) value(%s, %s, %s, %s, %s, %s, %s, %s)", (name, category, description, address, transport, mrt, latitude, longitude))
    # cursor.execute("insert into travel (name, category, images) value (%s,%s,%s)", (name, category, images))
    # cursor.execute("insert into travel (name) value ", (name))
    images = ','.join(images)
    cursor.execute("insert into travel (name, category, description, address, transport, mrt, latitude, longitude, images) value(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, category, description, address, transport, mrt, latitude, longitude, images))

    # query_string = 'INSERT INTO travel (name,images) VALUES (%s, %s);' ( name,var_string)
    # cursor.execute(query_string, images)


con.commit()
con.close()