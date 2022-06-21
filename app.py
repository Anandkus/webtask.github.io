

from flask import Flask, redirect,render_template,request,Response, session
import mysql.connector
import os #    for image upload 
from flask_mail import Mail, Message

app=Flask(__name__)
app.secret_key="anand" #sesssion

from datetime import date



UPLOAD_FOLDER = './static/upl'  #upl folder of image

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#for email 
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'srishtysaxena7@gmail.com',
    "MAIL_PASSWORD": 'srishty@24'
}
app.config.update(mail_settings)
mail = Mail(app)


#email 
@app.route("/m")
def mail11():
    return render_template("mail.html") 

    
# for email  
@app.route('/mail',methods=['POST'])
def email():
    subject = str(request.form['t1'])
    sender=str(request.form['t2'])
    
    with app.app_context():
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["srishtysaxena7@gmail.com"], # replace with your email for testing
                      body="This is a test email I sent with Gmail and Python!")
        mail.send(msg)
    


    return 'sucees'
    
 
  

#default website 
@app.route("/")
def indx():
    conn=mysql.connector.connect(host='localhost',user='root',password='anand@123',database='ananddb')
    cur=conn.cursor()
    cur.execute("select * from product")
    data=cur.fetchall()
    return render_template('index.html',item=data)
    

# admin navbar product
@app.route("/nav")
def nav_bar():
    return render_template("nav.html")    

@app.route("/form")
def product_form():
    return render_template("proForm.html")   

#product data insert

@app.route('/proform',methods=["POST"]) 
def product():
    #for image upload
    if 'file1' not in request.files:
        return 'there is no file1 in form!'
    file1 = request.files['file1']
    path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file1.save(path)
    pid=str(request.form['proId'])
    pname=str(request.form['proname'])
    price=str(request.form['price'])
    desc=str(request.form['desc'])
    
    #return file1.filename
    
    
    conn=mysql.connector.connect(host='localhost',user='root',password='anand@123',database='ananddb')

    cur=conn.cursor()
    cur.execute("insert into product(product_id,product_name,price,des,pic) values('"+pid+"','"+pname+"','"+price+"','"+desc+"','"+file1.filename+"')")
    conn.commit()
    return redirect("/showdata")


#show  all data  product
@app.route("/data")
def scrc():
    return render_template('searchList.html')
   
@app.route("/showdata")
def data_show():
    conn=mysql.connector.connect(host='localhost',user='root',password='anand@123',database='ananddb')
    cur=conn.cursor()
    cur.execute("select * from product")
    data=cur.fetchall()
    return render_template('searchList.html',item=data)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
#for data search
@app.route("/search",methods=["POST"])
def data_show1():
    conn=mysql.connector.connect(host='localhost',user='root',password='anand@123',database='ananddb')
    cur=conn.cursor()
    ser=str(request.form["se"])
    cur.execute("select * from product where product_name='"+ser+"'")
    data=cur.fetchall()
    return render_template('searchList.html',item=data)

#for delet data 
@app.route("/del")
def delete():
    id = request.args.get('id') 
    conn=mysql.connector.connect(host='localhost',user='root',password='anand@123',database='ananddb')
    cur=conn.cursor()
    cur.execute("delete from product where product_id="+str(id))
    conn.commit()
    cur.execute("select * from product")
    data=cur.fetchall()
    return render_template('searchList.html',item=data)

#for update data  
@app.route("/edit")
def upd():
    id = request.args.get('id') 
    conn=mysql.connector.connect(host='localhost',user='root',password='anand@123',database='ananddb')
    cur=conn.cursor()
    cur.execute("select * from product where product_id="+str(id))
    data=cur.fetchone()
    return render_template("update.html",data1=data)

# new update after product  
@app.route("/alter",methods=["POST"])
def alt():
    pid=str(request.form['proId'])
    pname=str(request.form['proname'])
    price=str(request.form['price'])
    desc=str(request.form['desc'])
 
    conn=mysql.connector.connect(host='localhost',user='root',password='anand@123',database='ananddb')

    cur=conn.cursor()
    cur.execute("update product set product_name='"+pname+"',price="+price+", des='"+desc+"' where product_id="+pid)
    conn.commit()
    return redirect("/showdata")



#addmin panel
@app.route("/ad")
def add():
    return render_template("admin.html") 


@app.route("/admin",methods=["POST"])
def add_info():
    user=str(request.form['t1'])
    pas=str(request.form['t2'])
    conn=mysql.connector.connect(host="localhost",user="root",password="anand@123",database="ananddb")
    cur=conn.cursor()
    cur.execute("select * from addmin where usid='"+user+"' and password='"+pas+"' ")
    
    if(cur.fetchone()):
        session["admin"]=user
        return render_template('nav.html')
    else:
        print("no")
        return render_template("admin.html")
 

  

#information all fani ..
@app.route("/info")
def info():
    return render_template("info.html")

#add card

@app.route("/cart")
def cardd():
    try:
        if session.get("user") :
            id = request.args.get('id') 
            conn=mysql.connector.connect(host='localhost',user='root',password='anand@123',database='ananddb')
            cur=conn.cursor()
            cur.execute("select * from product where product_id="+str(id))
            data=cur.fetchone()

            return render_template("cart.html",data1=data)
        else:
           
            return render_template("error.html")
    except Exception as e:
        
        return render_template("cart.html")



#cart data  insert

@app.route('/cartdata',methods=["POST"]) 
def cartdata():
   
    pname=str(request.form['pname'])
    price=str(request.form['price'])
    qty=str(request.form['qty'])
    cname=session["user"]
    cemail=session["email"]
    date1=date.today()
    d1 = date1.strftime("%d/%m/%Y")
    print("d1 =", d1)
    st='pending'
    p=int(price)
    q=int(qty)
    tot=p*q
    ta=str(tot)

    conn=mysql.connector.connect(host='localhost',user='root',password='anand@123',database='ananddb')

    cur=conn.cursor()
    cur.execute("insert into cart(pname,qty,price,cname,cemail,date1,states,total) values('"+pname+"',"+qty+" ,"+price+",'"+cname+"','"+cemail+"', '"+d1+"' ,'"+st+"' ,"+ta+" )")
    conn.commit()
    return redirect('/pay')


# payment 

@app.route("/pay")
def paymnt():
    return render_template('pay.html')

@app.route('/payment',methods=["POST"]) 
def paydetails():
   
    fname=str(request.form['flname'])
    em=str(request.form['em'])
    ed=str(request.form['ed'])
    city=str(request.form['city'])
    state=str(request.form['st'])
    code=str(request.form['code'])
    cardname=str(request.form['cardname'])
    cardnumber=str(request.form['carnumber'])
    month=str(request.form['month'])
    expyear=str(request.form['expyear'])
    cvv=str(request.form['cvv'])
    date1=date.today()
    d1 = date1.strftime("%d/%m/%Y")
   
   

    conn=mysql.connector.connect(host='localhost',user='root',password='anand@123',database='ananddb')

    cur=conn.cursor()
    cur.execute("insert into payment(fname,email,adress,city,state,zip,ncard,cardn,expm,expy,ccv,date) values('"+fname+"','"+em+"' ,'"+ed+"','"+city+"','"+state+"', '"+code+"' ,'"+cardname+"' ,'"+cardnumber+"' ,'"+month+"' ,'"+expyear+"','"+cvv+"','"+d1+"'  )")
    conn.commit()
    return 'succes '


# admin order show 
@app.route("/oder")
def order():
    conn=mysql.connector.connect(host='localhost',user='root',password='anand@123',database='ananddb')
    cur=conn.cursor()
    cur.execute("select * from payment")
    data=cur.fetchall()
    return render_template('ord.html',item=data)
    


#data user insert
@app.route("/web")
def res():
    return render_template("res.html")

@app.route("/save",methods=["POST"])
def save_date():
    nam=str(request.form['t1'])
    email=str(request.form['t2'])
    pas=str(request.form['t3'])
    conn=mysql.connector.connect(host="localhost",user="root",password="anand@123",database="ananddb")
    cur=conn.cursor()
    cur.execute("insert into web(name,email,password) values('"+nam+"','"+email+"','"+pas+"')")
    conn.commit()
    return render_template("login.html")

 #logout    

@app.route("/logout")
def log_out():
    
    session["user"]=None
    session["email"]=None
    return redirect("/")
    

# user login
@app.route("/log")
def log():
    return render_template("login.html")

@app.route("/log",methods=["POST"])
def log_info():
    email=str(request.form['t1'])
    pas=str(request.form['t2'])
    conn=mysql.connector.connect(host="localhost",user="root",password="anand@123",database="ananddb")
    cur=conn.cursor()
    cur.execute("select * from web where email='"+email+"' and password='"+pas+"' ")
    
    if(cur.fetchone()):
        cur.execute("select * from web where email='"+email+"' and password='"+pas+"' ")
        data=cur.fetchone()
        session["user"]=str(data[0])
        session["email"]=str(data[1])
        return redirect('/')
    else:
        return render_template("login.html")






if __name__=='__main__':
    app.run(debug=True)