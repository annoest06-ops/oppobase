from flask import Flask,request,redirect,url_for,session,render_template
import psycopg2
from psycopg2.extras import RealDictCursor
import os 


DATABASE_URL=os.getenv(
    "DATABASE_URL",
    "postgresql://postgres.icpadpcyltgtsqldhawq:husseinnkya22@aws-1-eu-central-1.pooler.supabase.com:6543/postgres",
)



app = Flask(__name__)
app.secret_key='mysecrete123'

@app.route('/visitor_reg',methods=['GET','POST'])
def visitor_register():
 
    if request.method=='POST':
        date=request.form.get('date')
        name=request.form.get('name')
        id_no=request.form.get('id_no')
        contact=request.form.get('contact')
        destiny=request.form.get('destiny')
        reason=request.form.get('reason')
        category=request.form.get('category')
        items=request.form.get('items')
        time_in=request.form.get('time_in')
        confirm=request.form.get('confirm')

        values=[date,name,id_no,contact,destiny,reason,category,items,time_in,confirm]
        success,error=visitor_get(values)

        if not success:
            
            print('error',error)
            return redirect(url_for('error'))

    return render_template('visitor.html')

def visitor_get(values):
    sql='''

    INSERT INTO visitor_table(date,name,sj_id,contact,destination,reason,category,item,time_in,sign)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)
    
@app.route('/student_reg',methods=['GET','POST'])
def student_regist():
    if request.method=='POST':
        date=request.form.get('date')
        name=request.form.get('name')
        form=request.form.get('form')
        reason=request.form.get('reason')
        permit=request.form.get('permit')
        time=request.form.get('time')
        status=request.form.get('status')
        confirm=request.form.get('confirm')

        values=[date,name,form,reason,permit,time,status,confirm]

        success,error=student_get(values)

        if not success:
            print('ERROR',error)
            return redirect(url_for('error'))

    return render_template('student.html')



def student_get(values):
    sql='''
    INSERT INTO student_table(date,name,form,reason,permission,created_time,status,sign_in)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
'''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)
 

@app.route('/staff_reg',methods=['GET','POST'])
def staff_regit():
    if request.method=='POST':
        date=request.form.get('date')
        name=request.form.get('name')
        status=request.form.get('status')
        time=request.form.get('time')
        confirm=request.form.get('confirm')

        values=[date,name,status,time,confirm]
        success,error=staff_get(values)
        
        if not success:
            print('ERROR',error)
            return redirect(url_for('error'))

    return render_template('staff.html')



def staff_get(values):
    sql='''
    INSERT INTO staff_table(date,name,status,time_out,sign_out)
    VALUES(%s,%s,%s,%s,%s)
'''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                 cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)
    

@app.route('/student_items',methods=['POST','GET'])
def student_item():
    if request.method=='POST':
         date=request.form.get('date')
         name=request.form.get('name')
         form=request.form.get('form')
         items=request.form.get('items')
         issued=request.form.get('issued')
         confirm=request.form.get('confirm')
         values=[date,name,form,items,issued,confirm]

         success,error=student_item_get(values)

         if not success:
             print('ERROR',error)
             return redirect(url_for('error'))
    return render_template('student_items.html')


    

def student_item_get(values):
    sql='''
    INSERT INTO student_item(date,name,form,item,issued,sign)
    VALUES(%s,%s,%s,%s,%s,%s)
'''
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                 cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)


@app.route('/school_items',methods=['POST','GET'])
def school_item():
    if request.method=='POST':
       date=request.form.get('date')
       name=request.form.get('name')
       item=request.form.get('item')
       status=request.form.get('status')
       time=request.form.get('time')
       confirm=request.form.get('confirm')
       values=[date,name,item,status,time,confirm]

       success,error=school_item_get(values)

       if not success:
           print('ERROR',error)
           return redirect(url_for('error'))
    
    return render_template('school_items.html')



def school_item_get(values):
    sql='''
   INSERT INTO school_item(date,name,item,status,time,sign)
   VALUES(%s,%s,%s,%s,%s,%s)
'''
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                 cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)


@app.route('/school_cars',methods=['POST','GET'])
def school_car():

    if request.method=='POST':
        date=request.form.get('date')
        name=request.form.get('name')
        car_no=request.form.get('car_no')
        status=request.form.get('status')
        time=request.form.get('time')
        confirm=request.form.get('confirm')
        values=[date,name,car_no,status,time,confirm]

        success,error=school_car_get(values)

        if not success:
            print('ERROR',error)
            return redirect(url_for('error'))

    return render_template('school_cars.html')


def school_car_get(values):
    sql='''
  INSERT INTO school_cars(date,name,car_no,status,time,sign)
  VALUES(%s,%s,%s,%s,%s,%s)
'''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                 cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)
    

@app.route('/private_cars',methods=['POST','GET'])
def private_car():

    if request.method=='POST':
        date=request.form.get('date')
        name=request.form.get('name')
        car_no=request.form.get('car_no')
        status=request.form.get('status')
        time=request.form.get('time')
        confirm=request.form.get('confirm')

        values=[date,name,car_no,status,time,confirm]
        success,error=private_car_get(values)

        if not success:
            print('ERROR',error)
            return redirect(url_for('error'))


            


    return render_template('private_cars.html')

def private_car_get(values):
    sql='''
  INSERT INTO private_cars(date,name,car_no,status,time,sign)
  VALUES(%s,%s,%s,%s,%s,%s)
'''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                 cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)


@app.route('/orders',methods=['POST','GET'])
def order():

    if request.method=='POST':
        date=request.form.get('date')
        details=request.form.get('details')
        time=request.form.get('time')
        confirm=request.form.get('confirm')

        values=[date,details,time,confirm]
        success,error=order_get(values)

        if not success:
            print('ERROR',error)
            return redirect(url_for('error'))
    return render_template('order.html')



def order_get(values):
    sql='''
  INSERT INTO order_table(date,details,time,sign)
  VALUES(%s,%s,%s,%s)
'''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                 cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)
    

@app.route('/org_property',methods=['POST','GET'])
def org_prop():

    if request.method=='POST':
        name=request.form.get('name')
        location=request.form.get('location')
        values=[name,location]

        success,error=org_prop_get(values)

        if not success:
            print('ERROR',error)
            return redirect(url_for('error'))

    return render_template('org_prop.html')

def org_prop_get(values):
    sql='''
   INSERT INTO org_items(item_name,location)
   VALUES(%s,%s)
'''
   
    try:
       with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                 cur.execute(sql,values)
            conn.commit()
       return True,None
    except Exception as e:
        return False,str(e)


@app.route('/student_check',methods=['POST','GET'])
def student_check():
    sets,error=student_check_give()
    if not sets:
        print('ERROR',error)

    
    if request.method=='POST':
        name=request.form.get('name')
        status=request.form.get('status_update')
        sign=request.form.get('sign')
        time=request.form.get('time_update')

        values=[time,status,sign,name]
        success,error=student_check_get(values)

        if not success:
            print('ERROR',error)
            return redirect(url_for('error'))

    return render_template('student_check.html',sets=sets)

def student_check_give():
    sql='''
     SELECT date,name,form,reason,permission,status,created_time
     FROM student_table 
     WHERE  status='in_temp' OR status='out_temp'
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql)
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return [],str(e)


def student_check_get(values):
    sql='''
    UPDATE student_table
    SET updated_time=%s, status=%s, sign_out=%s
    WHERE name=%s;
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)


@app.route('/visitor_check',methods=['GET','POST'])
def visitor_check():
    sets,error=visitor_check_give()

    if not sets:
        print('ERROR',error)

    if request.method=='POST':
        time_update=request.form.get('time_update')
        sign=request.form.get('sign')
        id_no=request.form.get('id_no')

        values=[time_update,sign,id_no]

        success,error=visitor_check_get(values)
        if not success:
            print('ERROR',error)
            return redirect(url_for('error'))

    return render_template('visitor_check.html', sets=sets)
def visitor_check_give():

    sql='''
    SELECT date,name,sj_id,contact,category,destination,reason,status,time_in
    FROM visitor_table
    WHERE status='IN'
    '''
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql)
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return [],str(e)
    
def visitor_check_get(values):
    sql='''
    UPDATE visitor_table
    SET time_out=%s, sign_out=%s, status='archieved'
    WHERE sj_id=%s;
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)



@app.route('/staff_check',methods=['POST','GET'])

def staff_checksforall():

    checks,error=staff_check_give()
    if not checks:
        print('ERROR',error)

    if request.method=='POST':
        name=request.form.get('name')
        time_in=request.form.get('time_in')
        sign_in=request.form.get('sign_in')

        values=[time_in,sign_in,name]
        cool,error=staff_check_get(values)

        if not cool:
            print('ERROR',error)
            return redirect(url_for('error'))

    return render_template('staff_check.html',checks=checks)

def staff_check_give():
    sql='''
    SELECT date,name,time_out
    FROM staff_table
    WHERE status='OUT'
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql)
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return False,str(e)


def staff_check_get(values):
    sql='''
      UPDATE staff_table
      SET time_in=%s ,sign_in=%s , status='IN'
      WHERE name=%s
    '''
    

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)


@app.route('/student_item_check',methods=['POST','GET'])
def st_items_check():
    passed,fail=student_item_check_give()

    if not passed:
        print('ERROR',fail)
        return redirect(url_for('error'))
    
    if request.method=='POST':
        staff_name=request.form.get('staff_name')
        st_name=request.form.get('st_name')
        date_update=request.form.get('date_update')
        sign=request.form.get('sign')
        
        values=[staff_name,sign,date_update,st_name]
        get,error=student_item_check_get(values)

        if not get:
            print('ERROR',error)

    return render_template('student_items_check.html',passed=passed)

    

def student_item_check_give():
  sql='''
  SELECT date,name,form,item
  FROM student_item
  WHERE status='FALSE'
  '''
  
  try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql)
                row=cur.fetchall()
            conn.commit()
        return row,None
  except Exception as e:
        return False,str(e)
   
    
def student_item_check_get(values):
    sql='''
    UPDATE student_item
    SET staff_name=%s ,sign_out=%s ,date_updated=%s ,status='TRUE'
    WHERE name=%s
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)
    
@app.route('/visitor_history',methods=['POST','GET'])
def v_hist():

    gets=None
    if request.method=='POST':
        date=request.form.get('date')

        gets,lose=visitor_hist(date)

        if not gets:
           print('ERROR',lose)
           return redirect(url_for('error'))
    return render_template('visitor_hist.html' ,gets = gets)

def visitor_hist(values):
    sql='''
    SELECT date,name,sj_id,contact,destination,reason,time_in,time_out,item,sign_in,category,sign_out
    FROM visitor_table
    WHERE date=%s
    '''
    
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(values,))
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return False,str(e)
    
@app.route('/student_history',methods=['POST','GET'])
def st_hist():
    
    cools=None
    if request.method=='POST':
      date=request.form.get('date')


      cools,error=student_hist(date)

      if not cools:
          print('ERROR',error)
          return redirect(url_for('error'))

    return render_template('student_hist.html' ,cools=cools)

def student_hist(values):
    sql='''
     SELECT date,name,form,reason,permission,status,created_time,sign_in,updated_time,sign_out
     FROM student_table
     WHERE date=%s
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(values,))
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return False,str(e)

@app.route('/school_cars_history',methods=['POST','GET'])
def scars_hist():

    
    if request.method=='POST':
        date=request.form.get('date')
        cools,error=school_car_hist(date)

        if not cools:
            print('ERROR',error)
            return redirect(url_for('error'))

    return render_template('scar_hist.html' , cools=cools)
    
def school_car_hist(values):
    sql='''
    SELECT date,name,car_no,time,status,sign
    FROM school_cars
    WHERE date=%s
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(values,))
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return False,str(e)
    
@app.route('/student_item_history',methods=['POST','GET'])
def st_item_hist():
    cools=None
    if request.method=='POST':
        date=request.form.get('date')
        cools,error=student_item_hist(date)

        if not cools:
            print('ERROR',error)
            return redirect(url_for('error'))


    
    return render_template('st_item_hist.html',cools=cools)

    
def student_item_hist(values):
    sql='''
    SELECT date,name,form,item,sign_in,sign_out,staff_name
    FROM student_item
    WHERE date=%s
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(values,))
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return False,str(e)

@app.route('/school_item_history',methods=['POST','GET'])
def sch_item_hist():
    
    if request.method=='POST':
        date=request.form.get('date')
        cools,error=school_item_hist(date)

        if not cools:
            print('ERROR',error)
            return redirect(url_for('error'))


    
    return render_template('school_item_hist.html',cools=cools)


def school_item_hist(values):
    sql='''
    SELECT date,name,item,time,status,sign
    FROM school_item
    WHERE date=%s
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(values,))
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return False,str(e)
    


@app.route('/private_car_history',methods=['POST','GET'])
def private_car_hist():
    cools=None
    if request.method=='POST':
        date=request.form.get('date')
        cools,error=private_car_hist(date)

        if not cools:
            print('ERROR',error)
            return redirect(url_for('error'))


    return render_template('private_car_hist.html',cools=cools)      




def private_car_hist(values):
    sql='''
    SELECT date,name,car_no,time,status,sign
    FROM private_cars
    WHERE date=%s
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(values,))
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return False,str(e)



@app.route('/order_history',methods=['POST','GET'])
def order_hist():
    cools=None
    if request.method=='POST':
        date=request.form.get('date')
        cools,error=order_hist(date)

        if not cools:
            print('ERROR',error)
            return redirect(url_for('error'))


    return render_template('order_hist.html',cools=cools)      




def order_hist(values):
    sql='''
    SELECT date,details,time,sign
    FROM order_table
    WHERE date=%s
    '''


    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(values,))
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return False,str(e)
    

@app.route('/org_check',methods=['POST','GET'])
def org_view():
   
        
    cools,error=org()

    if not cools:
        print('ERROR',error)
        return redirect(url_for('error'))


    return render_template('org_view.html',cools=cools)      

def org():
    sql='''
    SELECT item_name,location
    FROM org_items
     
    '''
   


    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql)
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return False,str(e)
    

@app.route('/report',methods=['POST','GET'])
def report():
    if request.method=='POST':
        date=request.form.get('date')
        shift=request.form.get('shift')
        detail=request.form.get('detail')
        comment=request.form.get('comment')
        time_in=request.form.get('time_in')
        sign_in=request.form.get('sign_in')

        values=[date,shift,detail,comment,time_in,sign_in]
        success,error=report_get(values)

        if not success:
            print('ERROR',error)
            return redirect(url_for('error'))

    return render_template('report.html')

@app.route('/report_check',methods=['POST','GET'])
def rp():

    sets=None
    if request.method=='POST':
        date=request.form.get('date')
        sets,error=report_check_give(date)

        if not sets:
            print('ERROR',error)
            return redirect(url_for('error'))
    
    return render_template('report_check.html', sets=sets)

@app.route('/update',methods=['POST','GET'])
def update_sent():
    if request.method=='POST':
        time_update=request.form.get('time_out')
        sign_out=request.form.get('sign_out')
        sign_in=request.form.get('sign_in')

        values=[time_update,sign_out,sign_in]
        success,error=report_update(values)

        if not success:
            print('ERROR',error)
            return redirect(url_for('error'))

    return render_template('report_check.html')
def report_check_give(values):
    sql='''
    SELECT date,shift,detail,comment,time_in,sign_in
    FROM report
    WHERE date=%s AND status='IN'
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(values,))
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return False,str(e)

def report_update(values):
    sql='''
   UPDATE report
    SET time_out=%s, sign_out=%s ,status='OUT'
    WHERE sign_in=%s AND status='IN'
'''
 
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                 cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)

def report_get(values):
    sql='''
    INSERT INTO report(date,shift,detail,comment,time_in,sign_in)
    VALUES(%s,%s,%s,%s,%s,%s)
'''
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor() as cur:
                 cur.execute(sql,values)
            conn.commit()
        return True,None
    except Exception as e:
        return False,str(e)


@app.route('/report_history',methods=['POST','GET'])
def report_histoy():
    cools=None
    if request.method=='POST':
        date=request.form.get('date')
        cools,error=report_hist(date)

        if not cools:
            print('ERROR',error)
            return redirect(url_for('error'))


    return render_template('report_hist.html',cools=cools)

def report_hist(values):
    sql='''
    SELECT date,detail,comment,time_in,sign_in,time_out,sign_out,shift
    FROM report
    WHERE date=%s
    '''

    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(values,))
                row=cur.fetchall()
            conn.commit()
        return row,None
    except Exception as e:
        return False,str(e)

@app.route('/login',methods=['POST','GET'])
def login_route():
    
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        values=[username,password]
        

        user,error=login_user(values)

        if not user:
            print('ERROR',error)
            return render_template('login.html',error='invalid credentials')
            

        if username==user['username'] and password==user['password']:
            session['username']=username
            return redirect(url_for('visitor_register'))

    return render_template('login.html')

def login_user(values):
    sql='''
    SELECT username,password
    FROM users
    WHERE username=%s AND password=%s
'''
    try:
        with psycopg2.connect(DATABASE_URL,sslmode="require") as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,values)
                row=cur.fetchone()
            conn.commit()
        return row,None
    except Exception as e:
        return False,None
    
@app.route('/error_fault')
def error():
    return render_template('error.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_route'))

if __name__=='__main__':
    app.run(debug=True)