import os
from flask import Flask, render_template, request, redirect, session, url_for, jsonify,flash
from os.path import join, dirname, realpath

from werkzeug.utils import secure_filename
from datetime import datetime
import csv
from flaskext.mysql import MySQL
from time import localtime
import string
from flask_mail import Mail, Message
import time

mysql = MySQL()
app = Flask(__name__)

# Mail server config.

app.config['MAIL_DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.ionos.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'testing@web-designpakistan.com'
app.config['MAIL_PASSWORD'] = 'Lawrence1234**'
app.config['MAIL_DEFAULT_SENDER'] = ('testing@web-designpakistan.com')

mail = Mail(app)



# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/formm'
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "ali"
app.config["MYSQL_DATABASE_HOST"] = "localhost"

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/images/')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
mysql.init_app(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.secret_key = "123456"


@app.route('/send-mail')
def send_mail():
	# try:
    msg = Message("Send Mail Tutorial!",recipients=["zohaibbuzdarr@gmail.com"])
    msg.html = "Yo!Have you heard the good word of Python???"           
    mail.send(msg)
    return 'Mail sent!'
	# except Exception as e:
	# 	return(str(e)) 


@app.route('/send-mail2')
def send_mail_2():
	# try:
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT customerdetail.name,customerdetail.email,(SELECT enddatee FROM hosting WHERE hosting.name = customerdetail.sno) as "End Date"FROM customerdetail INNER JOIN hosting ON customerdetail.sno = hosting.name;""")
    email = cur.fetchall()
    emails = []
    name = []
    for iii in email:
        name.append(iii)
    for i in email:
        emails.append(i)
    for ii in name:
        msg = Message("From Webtrica",recipients=[ii[1]])
        msg.html = f" Dear {ii[0]} Your Web Hosting Going To Expire On {ii[2]} Please Contact For Extension "           
        mail.send(msg)
    print(emails,"emailll")
    return redirect(url_for("homee"))
    
        



@app.route('/signin', methods =["POST", "GET"])
def signIn():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        print(name,username,password,"ZOHAIB")
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(''' insert into auth (name,username,password) values(%s,%s,%s);''',[name,username,password])
        conn.commit()
        cur.close()
        flash("Successfully Authentecated")
        return render_template("signin.html")
    else:
        return render_template("signin.html")


@app.route('/login', methods=["GET","POST"])
def loginn():
    if session.get("sessionusername"):
        return redirect(url_for("home"))
    else:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            print(username,password)
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(" select * from auth where username=%s;",[username])
            data = cur.fetchone()
            cur.close()
            conn.close()
            if data != None:
                if data[3] == password:
                    session["sessionusername"] = data[2]
                    session["timee"] = time.localtime() 


                    t = session.get("timee")
                    t = t
                    date_str = time.strftime("%Y-%m-%d %H:%M:%S", t)
                    print(date_str,"time")
                    name = session.get("sessionusername")
                    conn = mysql.connect()
                    cur = conn.cursor()
                    cur.execute(''' insert into logingtime (name,time) values(%s,%s);''',[name,date_str])
                    conn.commit()
                    cur.close()
                    
                    return redirect(url_for("home"))
                else:
                    session["error"] = "password doesn't match."
                    return redirect(url_for("loginn"))
            else:
                session["error"] = "user not exist."
                return redirect(url_for("loginn"))
        else:
            error = ""
            if session.get("error"):
                error = session.get("error")
                session.pop("error", None)
            return render_template("login.html", error=error)

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop("sessionusername", None)
    return redirect(url_for("loginn"))


@app.route('/home', methods =["POST", "GET"])
def home():
    if session.get("sessionusername"):
        if request.method == "POST":
            return redirect(url_for("home"))
        else:
            
            return render_template("basic.html")
    else:
        
        
        
        return redirect(url_for("loginn"))


@app.route('/dashboard', methods =["POST", "GET"])
def dashboard():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(""" SELECT COUNT(*) as "count" FROM customerdetail """)
    count = cur.fetchone()

    cur.execute(""" SELECT COUNT(*) as "count" FROM hosting """)
    hosting = cur.fetchone()


    cur.execute(""" SELECT month(enddatee) as "month" FROM hosting """)
    month = cur.fetchall()   
    time = localtime()
    time = time.tm_mon
    time = str(time)
    time = str(time)
    v = time.split("(")[0]
    print(type(time))
    print(v,"v")
    cur.execute(""" SELECT month(enddatee) as "month",customerdetail.name,hosting.sno FROM hosting INNER JOIN customerdetail ON customerdetail.sno = hosting.name WHERE month(hosting.enddatee) = %s """,[v])
    name = cur.fetchall()

    list =[]
    name = name
    for i in name:
        list.append(i)
    expire = len(list)


    cur = conn.cursor()
    cur.execute(""" SELECT COUNT(*) AS "Count" FROM `customer`""")
    project = cur.fetchone()
    




    conn.commit()
    cur.close()   
    return render_template("dashboard.html",count=count,hosting=hosting,expire=expire,project=project)


@app.route('/', methods =["POST", "GET"])
def homee():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(""" SELECT month(enddatee) as "month" FROM hosting """)
    month = cur.fetchall()   
    time = localtime()
    time = time.tm_mon
    time = str(time)
    time = str(time)
    v = time.split("(")[0]
    print(type(time))
    print(v,"v")
    cur.execute(""" SELECT month(enddatee) as "month",customerdetail.name,hosting.sno FROM hosting INNER JOIN customerdetail ON customerdetail.sno = hosting.name WHERE month(hosting.enddatee) = %s ORDER BY name LIMIT 2 """,[v])
    name = cur.fetchall()
    name = name
    for i in name:
        print(i,"zohaibbbbbs")

    cur.execute(""" SELECT month(enddatee) as "month",customerdetail.name,hosting.sno FROM hosting INNER JOIN customerdetail ON customerdetail.sno = hosting.name WHERE month(hosting.enddatee) = %s """,[v])
    shazu = cur.fetchone()
    print(shazu,"shazu")

    all_client = []
    for ii in name:
        all_client.append(ii)
    print(all_client,"allllllllll")
    

    listtt = []
    for item in all_client:
        item = str(item).split(",")[1]
        listtt.append(item)
        
    print(listtt,"07")
    
    def remove_punc(string):
        punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
        for ele in string:  
            if ele in punc:  
                string = string.replace(ele, "") 
        return string

    
    listtt = [remove_punc(i) for i in listtt]
    print(listtt)
    
    name = str(name)
    print(name,"hyder")
    name = name.split(",")[0]
    print(name,"pre")
    
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punc = ""
    for char in name:
        if char not in punctuations:
            no_punc = no_punc + char

    print(no_punc)
   
    print(name,"zzzzzz")
     
    if time == v:
        session["message"] = "hello Admin Your Customer "+no_punc+"'s" + "  Hosting Date Going To Expire In This Month "
        message = ""
        if session.get("message"):
            message = session.get("message")
            message = message 

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(""" SELECT COUNT(*) as "count" FROM customerdetail """)
    count = cur.fetchone()

    cur.execute(""" SELECT COUNT(*) as "count" FROM hosting """)
    hosting = cur.fetchone()
    conn.commit()
    cur.close()   

    
    
    return render_template("basic.html",list=listtt,name=all_client,count=count,hosting=hosting)

@app.route('/alert-list', methods =["POST", "GET"])
def alert_list():
    user_id = request.args.get("id")     
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT customerdetail.name,customerdetail.phone,hosting.disk,hosting.startdatee,hosting.enddatee,hosting.price,customerdetail.email,hosting.sno  FROM hosting INNER JOIN customerdetail on customerdetail.sno = hosting.name where hosting.sno=%s ;""",[user_id])
    client = cur.fetchall()
    head = ["Name","Phone","Data","Start Date","End Date","Price","email","Edit","Delete"]
    return render_template("alert-list.html",client=client,head=head)

@app.route('/hosting-list2', methods =["POST", "GET"])
def hosting_list2():
    user_id = request.args.get("id")     
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT customerdetail.name,customerdetail.phone,hosting.disk,hosting.startdatee,hosting.enddatee,hosting.price,customerdetail.email,hosting.sno  FROM hosting INNER JOIN customerdetail on customerdetail.sno = hosting.name ;""")
    client = cur.fetchall()
    head = ["Name","Phone","Data","Start Date","End Date","Price","email","Edit","Delete"]
    return render_template("hosting-list.html",client=client,head=head)


@app.route('/alert-list-all', methods =["POST", "GET"])
def alert_list_all():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(""" SELECT month(enddatee) as "month" FROM hosting """)
    month = cur.fetchall()   
    time = localtime()
    time = time.tm_mon
    time = str(time)
    time = str(time)
    v = time.split("(")[0]
    print(type(time))
    print(v,"v")
    cur.execute(""" SELECT customerdetail.name,customerdetail.phone,hosting.disk,hosting.startdatee,hosting.enddatee,hosting.price,month(hosting.enddatee) FROM hosting INNER JOIN customerdetail on customerdetail.sno = hosting.name WHERE month(hosting.enddatee) = %s  """,[v])
    name = cur.fetchall()
    name = name
    zo = []
    for zoo in name:
        zoo = zoo[6]
        zo.append(zoo)
    print(zo,"zooooo")
   

    all_client = []
    for ii in name:
        all_client.append(ii)
    print(all_client,"allllllllll")
    head = ["Name","Phone","Data","Start Date","End Date","Price"]
    return render_template("alert-list-all.html",head=head,all_client=all_client)



@app.route('/hosting-add', methods =["POST", "GET"])
def hosting_add():
    if request.method == "POST":
        client_name = request.form.get("name")            
        disk = request.form.get("disk")                     
        satart_date = request.form.get("startdate")            
        end_date = request.form.get("enddate")           
        price = request.form.get("price")           
        conn = mysql.connect()
        cur = conn.cursor()    
        cur.execute(''' insert into hosting (name,disk,startdatee,enddatee,price) values(%s,%s,%s,%s,%s);''',[client_name,disk,satart_date,end_date,price])
        conn.commit()
        cur.close()            
        session["message"] = "Project's Detail Has Been added successfully."
        message = ""
        if session.get("message"):
            message = session.get("message")
        print(message)


        msg = Message("New Deal! Bilkul Fresh", recipients=['zohaibbuzdar@gmail.com'])
        msg.html = str("New deal added on blilkul fresh.<br> ")
        mail.send(msg)

        return render_template("client-detail.html",message=message)
    else:
        conn = mysql.connect()
        cur = conn.cursor()    
        cur.execute(''' select * from customerdetail ''')
        data = cur.fetchall()
        conn.commit()
        cur.close() 

        return render_template("hosting-add.html",data=data)


@app.route('/hosting-list', methods =["POST", "GET"])
def hosting_list():  
    user_id = request.args.get("id")     
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT customerdetail.name,customerdetail.phone,hosting.disk,hosting.startdatee,hosting.enddatee,hosting.price,hosting.email FROM hosting INNER JOIN customerdetail on customerdetail.sno = hosting.name """)
    client = cur.fetchone()
    head = ["Name","Phone","Data","Start Date","End Date","Price","email"]
    return render_template("alert-list.html",client=client,head=head)



@app.route('/hosting-edit', methods =["POST", "GET"])
def hosting_edit():
    if request.method == "POST":
        sno = request.form.get("sno")  
        client_name = request.form.get("name")            
        disk = request.form.get("disk")            
        satart_date = request.form.get("startdate")            
        end_date = request.form.get("enddate")           
        price = request.form.get("price")           
        conn = mysql.connect()
        cur = conn.cursor()    
        cur.execute(''' update hosting set name=%s,disk=%s,startdatee=%s,enddatee=%s,price=%s where sno=%s ;''',[client_name,disk,satart_date,end_date,price,sno])
        conn.commit()
        cur.close()            
        session["message"] = "Project's Detail Has Been added successfully."
        message = ""
        if session.get("message"):
            message = session.get("message")
        print(message)
        return render_template("alert-list.html",message=message)
    else:
        userid = request.args.get("id")
        conn = mysql.connect()
        cur = conn.cursor()    
        cur.execute(''' SELECT customerdetail.name,customerdetail.phone,hosting.disk,hosting.startdatee,hosting.enddatee,hosting.price, hosting.sno FROM hosting INNER JOIN customerdetail on customerdetail.sno = hosting.name where hosting.sno = %s ''',[userid])
        data = cur.fetchone()

        cur.execute(''' SELECT hosting.sno,customerdetail.name,hosting.disk,customerdetail.sno FROM hosting INNER JOIN customerdetail on customerdetail.sno = hosting.name  ''')
        data2 = cur.fetchall()
        conn.commit()
        cur.close() 

        return render_template("hosting-edit.html",data=data,data2=data2)



@app.route('/client-detail', methods =["POST", "GET"])
def client_detail():
    if request.method == "POST":
        client_name = request.form.get("name")            
        country = request.form.get("country")            
        project_name = request.form.get("projectname")            
        phone = request.form.get("phone")           
        email = request.form.get("email")           
        conn = mysql.connect()
        cur = conn.cursor()    
        cur.execute(''' insert into customerdetail (name,country,phone,email) values(%s,%s,%s,%s);''',[client_name,country,phone,email])
        conn.commit()
        cur.close()            
        session["message"] = "Project's Detail Has Been added successfully."
        message = ""
        if session.get("message"):
            message = session.get("message")
        print(message)
        return render_template("client-detail.html",message=message)
    else:
        return render_template("client-detail.html")


@app.route('/client-list', methods =["POST", "GET"])
def client_list():       
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(" select * from customerdetail ")
    projects = cur.fetchall()

    conn.commit()
    cur.close()
    head = ["Customer Name","Country","Phone","Edit","email","Delete","View"] 
    return render_template("client-list.html",projects=projects,head=head)


@app.route('/client-edit', methods =["POST", "GET"])
def client_edit():
    if request.method == "POST":
        sno = request.form.get("sno")
        client_name = request.form.get("name")            
        country = request.form.get("country")            
        phone = request.form.get("phone")            
         
       
        conn = mysql.connect()
        cur = conn.cursor()
        
        
        cur.execute(''' Update customerdetail SET name=%s,country=%s,phone=%s where sno=%s;''',[client_name,country,phone,sno])
        conn.commit()
        cur.close()  

        session["message"] = "Project's Detail Has Been added successfully."
        message = ""    
        if session.get("message"):
            message = session.get("message")
        print(message)
        return redirect(url_for("client_list"))
    else:
        user_id = request.args.get("id")
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(" select * from customerdetail where sno=%s ",[user_id])
        data = cur.fetchone()
        conn.commit()
        cur.close()
        return render_template("client-edit.html",data=data)



@app.route('/client-delete', methods =["POST", "GET"])
def client_delete():
    user_id = request.args.get("id")
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(" delete from customerdetail where sno =%s",[user_id])
    conn.commit()
    cur.close()
    flash(" Data Has Been Deleted ")
    return redirect(url_for("client_list")) 



@app.route('/clients-project', methods =["POST", "GET"])
def clients_project():
    user_id = request.args.get("id")       
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT customer.projectname,customer.service,customer.extra,customer.price,customer.startdate,customer.enddate,customer.detail,customerdetail.name,customer.sno,customerdetail.sno FROM customerdetail INNER JOIN customer ON customer.customername = customerdetail.sno WHERE  customerdetail.sno = %s """,[user_id])
    projects = cur.fetchall()

    cur.execute(""" select * from customerdetail where sno=%s""",[user_id])
    name = cur.fetchone()

    cur.execute(""" select * from customer where sno=%s""",[user_id])
    id = cur.fetchone()
    print(id,"idd")

    conn.commit()
    cur.close()
    head = ["Project Name","Service","Extra","Price","Start Date","End Date","Detail","Edit","Delete"] 
    return render_template("clients-project-list.html",projects=projects,head=head,name=name,id=id)   
  




@app.route('/project-detail', methods =["POST", "GET"])
def project_detail():
    if request.method == "POST":
        client_name = request.form.get("name")            
         
        project_name = request.form.get("projectname")            
        service = request.form.get("service")            
        project_price = request.form.get("projectprice")            
                 
        start_date = request.form.get("startdate")            
        end_date = request.form.get("enddate")            
        project_detail = request.form.get("detail")            
        extra = request.form.get("extra")            
       
        conn = mysql.connect()
        cur = conn.cursor()
     
       
       
        
        cur.execute(''' insert into customer (customername,projectname,service,price,startdate,enddate,detail,extra) values(%s,%s,%s,%s,%s,%s,%s,%s);''',[client_name,project_name,service,project_price,start_date,end_date,project_detail,extra])
        conn.commit()
        cur.close()
            
        session["message"] = "Project's Detail Has Been added successfully."
        message = ""
        if session.get("message"):
            message = session.get("message")
        print(message)
        return render_template("customer-detail.html",message=message)
    
            
    else:
        conn = mysql.connect()
        cur = conn.cursor()

        cur.execute(" select * from customerdetail ")
        data = cur.fetchall()
        print(data,"zohaib")
        

        conn.commit()
        cur.close()

        return render_template("customer-detail.html",data=data)


@app.route('/projects-list', methods =["POST", "GET"])
def projects_list():       
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(""" SELECT customer.sno,customerdetail.name,customer.service,customerdetail.country,customer.projectname,customer.price,customerdetail.phone,customer.startdate,customer.enddate,customer.detail,customer.extra FROM customer INNER JOIN customerdetail ON customerdetail.sno = customer.customername """)
    projects = cur.fetchall()

    conn.commit()
    cur.close()
    head = ["Customer Name","Services","Country","Project Name","Price","Phone","Start Date","End Date","detail","Extra","Edit","Delete"] 
    return render_template("projects-list.html",projects=projects,head=head)


@app.route('/project-edit', methods =["POST", "GET"])
def project_edit():
    if request.method == "POST":
        sno = request.form.get("sno")
        print(sno,"snooo")
        client_name = request.form.get("name")            
        service = request.form.get("service")            
               
        project_name = request.form.get("projectname")            
        project_price = request.form.get("projectprice")            
              
        start_date = request.form.get("startdate")            
        end_date = request.form.get("enddate")            
        project_detail = request.form.get("detail")   
        extra = request.form.get("extra")   
        print(sno,client_name,service,project_name,project_price,start_date,end_date,project_detail,extra)
       
        conn = mysql.connect()
        cur = conn.cursor()
        
        
        cur.execute(''' Update customer SET customername=%s,service=%s,projectname=%s,price=%s,startdate=%s,enddate=%s,detail=%s,extra=%s where sno=%s;''',[client_name,service,project_name,project_price,start_date,end_date,project_detail,extra,sno])
        conn.commit()
        cur.close()  

        session["message"] = "Project's Detail Has Been added successfully."
        message = ""    
        if session.get("message"):
            message = session.get("message")
        print(message)
        return redirect(url_for("projects_list"))
    else:
        user_id = request.args.get("id")
        conn = mysql.connect()
        cur = conn.cursor()

        cur.execute(""" SELECT customer.projectname,customer.service,customer.extra,customer.price,customer.startdate,customer.enddate,customer.detail,customerdetail.name,customer.sno,customerdetail.sno FROM customerdetail INNER JOIN customer ON customer.customername = customerdetail.sno WHERE  customerdetail.sno = %s or customer.sno = %s """,[user_id,user_id])
        projects = cur.fetchone()
        print(projects)

        cur.execute(""" select * from customerdetail """ )
        projects2 = cur.fetchall()
        conn.commit()
        cur.close()
        return render_template("project-edit.html",data=projects,data2=projects2)

   



@app.route('/project-delete', methods =["POST", "GET"])
def category_delete():
    user_id = request.args.get("id")
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(" delete from customer where sno =%s",[user_id])
    conn.commit()
    cur.close()
    flash(" Data Has Been Deleted ")
    return redirect(url_for("projects_list"))    

@app.route('/add-product', methods =["POST", "GET"])
def addProduct():
    if request.method == "POST":
        company = request.form.get("company")
        pname = request.form.get("pname")
        ptype = request.form.get("ptype")
        pprice = request.form.get("pprice")
        print(pname,ptype,pprice,"ZOHAIB")
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(''' insert into product (pname,ptype,pprice,company) values(%s,%s,%s,%s);''',[pname,ptype,pprice,company])
        conn.commit()
        cur.close()
        error = 'Invalid username or password. Please try again!'
        return render_template("add-product.html",error=error)
    else:
        return render_template("add-product.html")


@app.route('/country-list', methods =["POST", "GET"])
def country_list():       
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("""SELECT DISTINCT country as "country", count(country) as "count"
FROM customerdetail group BY customerdetail.country ;""")
    country = cur.fetchall()

    conn.commit()
    cur.close()
    head = ["Country","Total Client","View"] 
    return render_template("country-list.html",country=country,head=head)


@app.route('/country-user-list', methods =["POST", "GET"])
def country_user_list():
    user_id = request.args.get("id")       
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(""" SELECT * FROM customerdetail where customerdetail.country=%s ;""",[user_id])
    all_users = cur.fetchall()

    conn.commit()
    cur.close()
    head = ["Customer Name","Country","Phone","email"] 

    return render_template("country-user-list.html",all_users=all_users,head=head)




@app.route("/user-login-time")
def user_loging_time():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(""" SELECT * FROM logingtime ;""")
    all_users = cur.fetchall()
    head = ["Name","Time","Delete"]

    conn.commit()
    cur.close()
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print(ip,"ippp")
    
    return render_template("user-loging-time.html",all_users=all_users,head=head)


@app.route("/user-login-time-delete")
def user_loging_time_delete():
    userId = request.args.get("id")
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(" delete from logingtime where sno=%s ",[userId])
    conn.commit()
    cur.close()
    return redirect(url_for("user_loging_time"))





@app.route('/maintenance-add', methods =["POST", "GET"])
def maintenance_add():
    if request.method == "POST":
        client_name = request.form.get("name")            
        project_name = request.form.get("pname")                     
        maintenance_detail = request.form.get("maintenance")                     
        price = request.form.get("price")           
        conn = mysql.connect()
        cur = conn.cursor()    
        cur.execute(''' insert into maintenance (clientname,projectname,detail,price) values(%s,%s,%s,%s);''',[client_name,project_name,maintenance_detail,price])
        conn.commit()
        cur.close()            
        session["message"] = "Project's Maintenance Detail Has Been added successfully."
        message = ""
        if session.get("message"):
            message = session.get("message")
        print(message)


        # msg = Message("New Deal! Bilkul Fresh", recipients=['zohaibbuzdar@gmail.com'])
        # msg.html = str("New deal added on blilkul fresh.<br> ")
        # mail.send(msg)

        return render_template("maintenance-add.html",message=message)
    else:
        conn = mysql.connect()
        cur = conn.cursor()    
        cur.execute(''' select * from customerdetail ''')
        data = cur.fetchall()
        conn.commit()
        cur.close() 

        return render_template("maintenance-add.html",data=data)


@app.route('/maintenance-list', methods =["POST", "GET"])
def maintenance_list():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(""" SELECT maintenance.sno, customerdetail.name,maintenance.projectname,maintenance.detail,maintenance.price FROM maintenance INNER JOIN customerdetail ON customerdetail.sno = maintenance.clientname ;""")
    maintenance = cur.fetchall()
    head = ["Client Name","Project Name","Maintenance Detail","Price","Edit","Delete"]

    
    return render_template("maintenance-list.html",maintenance=maintenance,head=head)





@app.route('/maintenance-edit', methods =["POST", "GET"])
def maintenance_edit():
    if request.method == "POST":
        sno = request.form.get("sno") 
        client_name = request.form.get("name")            
        project_name = request.form.get("pname")                     
        maintenance_detail = request.form.get("maintenance")                     
        price = request.form.get("price") 
        print(sno,client_name,project_name,maintenance_detail,price,"heloooooo")          
        conn = mysql.connect()
        cur = conn.cursor()    
        cur.execute(''' update maintenance set clientname=%s,projectname=%s,detail=%s,price=%s where sno=%s ;''',[client_name,project_name,maintenance_detail,price,sno])
        conn.commit()
        cur.close()            
        session["message"] = "Project's Detail Has Been added successfully."
        message = ""
        if session.get("message"):
            message = session.get("message")
        print(message)


        # msg = Message("New Deal! Bilkul Fresh", recipients=['zohaibbuzdar@gmail.com'])
        # msg.html = str("New deal added on blilkul fresh.<br> ")
        # mail.send(msg)

        return redirect(url_for("maintenance_list"))
    else:
        user_id = request.args.get("id")
        conn = mysql.connect()
        cur = conn.cursor()    
        cur.execute(''' select * from customerdetail ''')
        data2 = cur.fetchall()

        cur.execute(''' SELECT maintenance.sno, customerdetail.name,maintenance.projectname,maintenance.detail,maintenance.price,customerdetail.sno FROM maintenance INNER JOIN customerdetail ON customerdetail.sno = maintenance.clientname where maintenance.sno=%s ''',[user_id])
        data = cur.fetchone()


        conn.commit()
        cur.close() 

        return render_template("maintenance-edit.html",data=data,data2=data2)



@app.route('/maintenance-delete', methods =["POST", "GET"])
def maintenance_delete():   
    userId = request.args.get("id")
    print(userId)
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(""" delete from maintenance WHERE sno=%s;""",[userId])
    conn.commit()
    cur.close()
    return redirect(url_for("maintenance_list"))




@app.route('/calls-add',methods =["POST", "GET"])
def calls_add():
    if request.method == "POST":
        name = request.form.getlist("name")            
        number = request.form.getlist("phone")                 
        reason = request.form.getlist("reason")                     
        country = request.form.getlist("country")           
        city = request.form.getlist("city")           
        date = request.form.getlist("date")   
        print(name)
        print(number, reason, country, city, date)
        for index,item in enumerate(name):
            names = item
            phoneNumber = number[index]
            reasons = reason[index]
            countries = country[index]
            cities = city[index]
            dates = date[index]

            
        
            conn = mysql.connect()
            cur = conn.cursor()  
        
            cur.execute(""" insert into calls (name,number,reason,country,city,date) values (%s,%s,%s,%s,%s,%s)""", [names,phoneNumber,reasons,countries,cities,dates])
        
            conn.commit()
            cur.close()            
        session["message"] = "Customers Who has Phone Call Us Has Been added successfully."
        message = ""
        if session.get("message"):
            message = session.get("message")
        print(message)


        # msg = Message("New Deal! Bilkul Fresh", recipients=['zohaibbuzdar@gmail.com'])
        # msg.html = str("New deal added on blilkul fresh.<br> ")
        # mail.send(msg)

        return render_template("calls-add.html",message=message)
    else:
        conn = mysql.connect()
        cur = conn.cursor()    
        cur.execute(''' select * from customerdetail ''')
        data = cur.fetchall()
        conn.commit()
        cur.close() 

        return render_template("calls-add.html",data=data)


@app.route('/calls-list',methods =["POST", "GET"])
def calls_list():
    conn = mysql.connect()
    cur = conn.cursor()    
    cur.execute(''' select * from calls ''')
    calls = cur.fetchall()
    conn.commit()
    cur.close() 
    header = ["Name","Number","Reason","Country","City","Date","Edit","Delete"]
    return render_template("call-list.html",calls=calls,header=header)



@app.route('/calls-edit',methods =["POST", "GET"])
def calls_edit():
    if request.method == "POST":
        name = request.form.getlist("name")            
        sno = request.form.getlist("sno")            
        number = request.form.getlist("phone")                 
        reason = request.form.getlist("reason")                     
        country = request.form.getlist("country")           
        city = request.form.getlist("city")           
        date = request.form.getlist("date")   
        print(name)
        print(number, reason, country, city, date)
        

            
        
        conn = mysql.connect()
        cur = conn.cursor()  
        
        cur.execute(""" update calls set name=%s,number=%s,reason=%s,country=%s,city=%s,date=%s where sno=%s""", [name,number,reason,country,city,date,sno])
        
        conn.commit()
        cur.close()            
        session["message"] = "Data Has Been Updated"
        message = ""
        if session.get("message"):
            message = session.get("message")
        print(message)


        # msg = Message("New Deal! Bilkul Fresh", recipients=['zohaibbuzdar@gmail.com'])
        # msg.html = str("New deal added on blilkul fresh.<br> ")
        # mail.send(msg)

        return redirect("/calls-list")
    else:
        user_id = request.args.get("id")
        conn = mysql.connect()
        cur = conn.cursor()    
        cur.execute(''' select * from customerdetail ''')
        data = cur.fetchall()
        cur.execute(''' select * from calls where sno=%s ''',[user_id])
        calls = cur.fetchone()
        conn.commit()
        cur.close() 

        return render_template("call-edit.html",data=data,calls=calls)


@app.route('/calls-delete',methods =["POST", "GET"])
def calls_delete():
    user = request.args.get("id")
    conn = mysql.connect()
    cur = conn.cursor()    
    cur.execute(''' delete from calls where sno =%s ''',[user])
    data = cur.fetchall()
    conn.commit()
    cur.close() 
    return redirect("calls-list")




if __name__=="__main__":
    app.run(debug=True, port=2001)