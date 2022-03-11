from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import jsonify
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
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="website"
    )
    # print(id)
    # print(type(id))
    PageId=int(''.join(map(str, id)))
    # print(PageId)
    # print(type(PageId))

    mycursor = mydb.cursor()
    mycursor.execute("select count(*) from travel ")
    total = mycursor.fetchone()
    total=int(''.join(map(str, total)))
    # print(total)
    # print(type(total))
    try:
        if PageId<=total:
            mycursor = mydb.cursor()
            mycursor.execute("select json_object('id', id,'name', name,'category', category,'description', description,'address', address,'transport', transport,'mrt', mrt,'latitude', latitude,'longitude', longitude,'images', images) from travel where id = %s ", (id,))
            results = mycursor.fetchone()
            print(results)
            print(type(results))
            #取出來是tuple


            # tuple轉str
            results = ",".join('%s' %id for id in results)
            # print(results)
            # print(type(results))
            
            #原本預計轉dict但還是str
            # eval(results),type(eval(results))
            # print(results)
            # print(type(results))

            #str轉dic
            dic={"data":eval(results)}

            #[key:images] str轉list
            dic["data"]["images"]=list(dic["data"]["images"].split(","))
            # print(dic["data"]["images"])
            # print(type(dic["data"]["images"]))
            # print(type(dic))

            return dic
            return render_template("attraction.html")
        elif PageId>total:
            dic={"error": True,"message": "頁碼錯誤"}
            return dic,400
        
    except:
        dic={"error": True,"message": "自訂的錯誤訊息"}
        return dic,500
        


@app.route("/attractions", methods=["get"])
def attractions():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="website"
    )
    page = request.args.get("page", default = 0, type = int)
    keyword = request.args.get("keyword", default='*', type = str)


    mycursor = mydb.cursor()
    startPage = page*12
    print(keyword)
    print(page)
    if keyword != '*':
        try:
            mycursor.execute("select count(*) from travel where name like concat( '%', %s, '%')",(keyword,))
            total = mycursor.fetchone()
            total=int(''.join(map(str, total)))
            # print(total)
            # print(type(total))
            # print(total)
            totalPage=total/12
            # print(totalPage)
            totalPage=math.ceil(totalPage)
            # print("totalPage:"+str(totalPage))
            # print(type(totalPage))
            mycursor.execute("select json_object('id', id,'name', name,'category', category,'description', description,'address', address,'transport', transport,'mrt', mrt,'latitude', latitude,'longitude', longitude,'images', images) from travel where name like concat( '%', %s, '%') limit %s , 12 ", (keyword,startPage))
            results = mycursor.fetchall()
            # print(results)
            # print(type(results))

            results = ",".join('%s' %id for id in results)
            # print(results)
            # print(type(results))
            dic={"data":eval(results)}

            #quantity per page
            # print(len(dic["data"]))
            # print(type(len(dic["data"])))
            for i in range(len(dic["data"])):
                dic["data"][i]["images"]=list(dic["data"][i]["images"].split(","))

            
            # print(results)
            # print(type(results))
            
            if page<totalPage-1:
                dic["nextPage"]=page+1
                
                return dic
            elif page == totalPage-1:
                
                dic["nextPage"]=None
                return dic

            mydb.close()
        except:
            dic={"error": True,"message": "自訂的錯誤訊息"}
            return dic,500
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
            results = mycursor.fetchall()
            print(results)
            print(type(results))

            #list轉str
            results = ",".join('%s' %id for id in results)
            print(results)
            print(type(results))

            # eval(results),type(eval(results))
            # print(results)
            # print(type(results))
            dic={"data":eval(results)}
            # print(len(dic["data"]))
            # print(type(len(dic["data"])))
            for i in range(len(dic["data"])):
                dic["data"][i]["images"]=list(dic["data"][i]["images"].split(","))
            # print(dic["data"][0]["images"])
            # print(type(dic["data"][0]["images"]))
            # print(dic)
            # print(type(dic))
            if page<totalPage-1:
                dic["nextPage"]=page+1
                # print(dic["data"][0]["images"])
                # print(dic)
                # print(type(dic))
                return dic
            elif page == totalPage-1:
                dic["nextPage"]=None
                return dic
            mydb.close()
        except:
            dic={"error": True,"message": "自訂的錯誤訊息"}
            return dic,500

@app.route("/booking")
def booking():
    return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

app.add_url_rule('/api/attraction/<id>',
                 endpoint="attractions/<id>", view_func=attraction)
app.add_url_rule('/api/attractions', endpoint="attractions",
                 view_func=attractions)
if __name__ == "__main__":
    # app.debug = True
    app.run(host='0.0.0.0', port=3000)











