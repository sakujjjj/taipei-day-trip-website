from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import jsonify
from flask_paginate import Pagination,get_page_parameter
import mysql.connector
import json
import math

##防止null
global null
null=''

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")


@app.route("/api/attractions", methods=["get"])
def attractions():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="03082002",
    database="website"
    )
    page = request.args.get("page", default = 1, type = int)
    keyword = request.args.get("keyword", default='*', type = str)
    
    
    mycursor = mydb.cursor()
    startPage = (page-1)*12
    # print(keyword)
    # print(page)
    if keyword != '*':
        try:
            mycursor.execute("select count(*) from travel where name like concat( '%', %s, '%')",(keyword,))
            total = mycursor.fetchone()
            total=int(''.join(map(str, total)))
            print(total)
            print(type(total))
            print(total)
            totalPage=total/12
            # print(totalPage)
            totalPage=math.ceil(totalPage)
            print("totalPage:"+str(totalPage))
            print(type(totalPage))

            # mycursor.execute("select json_object('id', id,'name', name,'category', category,'description', description,'address', address,'transport', transport,'mrt, mrt,'latitude', latitude,'longitude', longitude,'images', images) from travel where name like concat( '%', %s, '%') limit %s , 12 ", (keyword,startPage))
            mycursor.execute("select json_object('id', id,'name', name,'category', category,'description', description,'address', address,'transport', transport,'mrt', mrt,'latitude', latitude,'longitude', longitude,'images', images) from travel where name like concat( '%', %s, '%') limit %s , 12 ", (keyword,startPage))
            results = mycursor.fetchall()
            print(results)
            print(type(results))

            results = ",".join('%s' %id for id in results)
            print(results)
            print(type(results))

            eval(results),type(eval(results))
            print(results)
            print(type(results))
            # dic={"nextPage": page+1, "data":eval(results)}
            if page<totalPage:
                dic={"nextPage": page+1, "data":eval(results)}
                return dic
            elif page == totalPage:
                dic={"nextPage": None, "data":eval(results)}
                return dic
            # return dic
            # return "ok"
            mydb.close()
        except:
            dic={"error": True,"message": "自訂的錯誤訊息"}
            return dic
    else:
        try:
            # print(get_page_parameter())
            # page=request.args.get(get_page_parameter(),type=int,default=1)
            # print(page)
            mycursor.execute("select count(*) from travel ")
            total = mycursor.fetchone()
            total=int(''.join(map(str, total)))
            # print(total)
            # print(type(total))

            totalPage=total/12
            # print(totalPage)
            totalPage=math.ceil(totalPage)
            # print("totalPage:"+str(totalPage))
            # print(type(totalPage))

            mycursor.execute("select json_object('id', id,'name', name,'category', category,'description', description,'address', address,'transport', transport,'mrt', mrt,'latitude', latitude,'longitude', longitude,'images', images) from travel limit %s , 12 ", (startPage,))
            # mycursor.execute("select json_object('id', id,'name', name, 'mrt', mrt) from travel limit %s , 12 ", (startPage,))
            results = mycursor.fetchall()
            # print(results)
            # print(type(results))

            results = ",".join('%s' %id for id in results)
            # print(results)
            # print(type(results))

            # eval(results),type(eval(results))
            # print(results)
            # print(type(results))


            if page<totalPage:
                dic={"nextPage": page+1, "data":eval(results)}
                return dic
            elif page == totalPage:
                dic={"nextPage": None, "data":eval(results)}
                return dic
            
            mydb.close()
        except:
            dic={"error": True,"message": "自訂的錯誤訊息"}
            return dic







@app.route("/api/attraction/<id>", methods=["get"])
def attractionId(id):
	mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="03082002",
	database="website"
	)
	mycursor = mydb.cursor()
	mycursor.execute("select json_object('id', id,'name', name,'category', category,'description', description,'address', address,'transport', transport,'mrt', mrt,'latitude', latitude,'longitude', longitude,'images', images) from travel where id = %s ", (id,))
	results = mycursor.fetchone()
	print(results)
	print(type(results))

	results = ",".join('%s' %id for id in results)
	print(results)
	print(type(results))

	eval(results),type(eval(results))
	print(results)
	print(type(results))
	dic={"data":eval(results)}
	print(type(dic))
	return dic

@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.debug = True
app.run(port=3000)











