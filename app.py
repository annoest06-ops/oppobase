<<<<<<< HEAD
# This codes where written by me hussein martin nkya from 24/8/2026
# I pray to God that this project to impact thousands of students in Tanzania and Africa in large

from flask import Flask ,request,redirect,url_for,session,render_template
import atexit
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL')
SECRET_KEY=os.getenv('SECRET_KEY')

# Global connection pool initialization
db_pool = ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DATABASE_URL,
    sslmode="require")
    
# Automatically close all pooled connections when app stops
@atexit.register
def close_db_pool():
    if db_pool:
        db_pool.closeall()


app = Flask(__name__)
app.secret_key=SECRET_KEY

# i ended here for today so we will start from tomorrow
@app.route('/login',methods=['POST','GET'])
def sign_in():
    if request.method=='POST':
        action=request.form.get('action')

        if action=='login':
            pass

    return render_template('login.html')

def user_login():
    sql='''
    
'''

@app.route('/new_content',methods=['POST','GET'])
def create_content():
    if request.method=='POST':
        topic_number=request.form.get('topic_no')
        topic_name=request.form.get('topic_name')
        topic_body=request.form.get('content')
        topic_example=request.form.get('example')

        values=[topic_number,topic_name,topic_body,topic_example]

        success,error=insert_content(values)

        if not success:
            print('error:',error)
        else:
            print('successfull content added')

    
    return render_template('create_content.html')
def insert_content(values):
    sql='''
    INSERT INTO content(topic_number,topic_name,content_body,example)
    VALUES(%s,%s,%s,%s)
'''

    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(sql, values)
        conn.commit()
        return True, None
    except Exception as e:
        if conn:
            conn.rollback()
        return False, str(e)
    finally:
        if conn:
            db_pool.putconn(conn)
    
def topic_select():
    sql='''
    SELECT topic_number,topic_name 
    FROM content
'''
    conn=None
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows, None
    except Exception as e:
        if conn:
            conn.rollback()
        return [], str(e)
    finally:
        if conn:
            db_pool.putconn(conn)

@app.route('/new_eg',methods=['POST','GET'])
def create_eg():
    if request.method=='POST':
        topic=request.form.get('topic')
        name=request.form.get('eg_name')
        country=request.form.get('country')
        apply_to=request.form.get('apply_to')
        skills=request.form.get('apply_to')
        achieve=request.form.get('achieve')
        avatar=request.form.get('avatar')
        question=request.form.get('question')
        response=request.form.get('response')
        word_count=request.form.get('word_count')
        eg_no=request.form.get('eg_no')
        comment=request.form.get('comment')

        values=[name,country,apply_to,skills,achieve,avatar,question,response,eg_no,comment,topic,word_count]
        success,error=new_example(values)

        if not success:
            print('ERROR',error)
        else:
            print('successfull example added')

    list_topic,error=topic_select()

    if not list_topic:
        print('ERROR',error)


    return render_template('create_eg.html',topic_list=list_topic)


def new_example(values):
    sql='''
  INSERT INTO example(name,country,college,skills,achieves,avatar,question,response,example_no,comment,topic_id,word_count)
  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
'''
    
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(sql, values)
        conn.commit()
        return True, None
    except Exception as e:
        if conn:
            conn.rollback()
        return False, str(e)
    finally:
        if conn:
            db_pool.putconn(conn)

@app.route('/edit_content',methods=['POST','GET'])
def content_edit():
     
    search=[]
    error=None
    get_content=[]

    search,error=topic_select()

    if not search:
           print('fail to load names',error)

    if request.method=='POST':

        action=request.form.get('action')

        if action=='search_by_name':
            name=request.form.get('topic_name')

            get_content,error=name_search_content(name)

            if not get_content:
               print('ERROR',error)

        if action=='update_from_name':
            topic_name=request.form.get('topic_name')
            topic_number=request.form.get('topic_number')
            content_body=request.form.get('body')
            example=request.form.get('example')
            content_id=request.form.get('content_id')

            success,error=update_content(topic_name,topic_number,content_body,example,content_id)

            if not success:
                print('FAIL TO UPDATE',error)
 
    return render_template('edit_content.html',search_name=search,content=get_content)


def name_search_content(name):
    sql='''
   SELECT topic_number,topic_name,content_body,example,id
   FROM content
   WHERE topic_name=%s;
'''

    conn = None
   
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(name,))
                row=cur.fetchone()
        
        return row,None
    except Exception as e:
        if conn:
            conn.rollback()
        return [], str(e)
    finally:
        if conn:
            db_pool.putconn(conn)

def update_content(topic_number,topic_name,content_body,example,content_id):
    sql='''
    UPDATE content 
    SET topic_number = %s, topic_name = %s, content_body = %s ,example=%s
    WHERE id = %s 
    RETURNING topic_number, topic_name, content_body,example,id;
'''
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql,(topic_name,topic_number,content_body,example,content_id))
            row=cur.fetchone()
            
        conn.commit()   
        return row,None
    except Exception as e:
            if conn:
                conn.rollback()
            return [], str(e)
    finally:
            if conn:
                db_pool.putconn(conn)


@app.route('/update_example',methods=['POST','GET'])
def edit_update():
    search=[]
    success={}
    error=None

    search,error=topic_select()
    
    if not search:
        print('fail to load topics',error)

    if request.method=='POST':
        action=request.form.get('action')

        if action=='search_example':
            name=request.form.get('topic_name')
            example=request.form.get('example_number')

            success,error=content_example(name,example)

            if not success:
                 print('Fail to access the value')



    return render_template('edit_example.html',eg_name=search,eg_value=success)

def content_example(topic_id,example_no):
    sql='''
    SELECT name,country,college,skills,achieves,avatar,question,response,example_no,comment,topic_id,word_count
    FROM example
    WHERE topic_id=%s AND example_no=%s;
    
'''        
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (topic_id,example_no))
            row = cur.fetchone()
        return row, None
    except Exception as e:
        if conn:
            conn.rollback()
        if conn and isinstance(e, (psycopg2.OperationalError, psycopg2.InterfaceError)):
            conn.close()
            conn = None
        return None, str(e)
    finally:
        if conn:
            db_pool.putconn(conn)
    
        
def edit_example(name,country,college,skills,achieves,avatar,question,response,comment,word_count,topic_id,example_no):
    sql='''
    UPDATE example
    SET name = %s ,country = %s,college = %s,skills = %s,achieves = %s,avatar = %s,question = %s,response = %s,example_no = %s,comment = %s,topic_id = %s,word_count = %s
    WHERE  topic_id = %s AND example_no = %s;
'''
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(sql, (name, country, college, skills, achieves, avatar,
                               question, response, example_no, comment, topic_id, word_count,
                               topic_id, example_no))
        conn.commit()
        return True, None
    except Exception as e:
        if conn:
            conn.rollback()
        if isinstance(e, (psycopg2.OperationalError, psycopg2.InterfaceError)):
            conn.close()
            conn = None
        return False, str(e)
    finally:
        if conn:
            db_pool.putconn(conn)



@app.route('/tuto_dash',methods=['POST','GET'])
def tdash():
    
    
    tp_summary,error=tp_sum()
    if not tp_summary:
        print('Fail to analyze topic',error)

    success=None
    if request.method=='POST':
        tp_id=request.form.get('topic_ref')

        if tp_id:
            return redirect(url_for('tuto_home',topic_id=tp_id))

        success,error=select_topic(tp_id)

        if not success:
            print('fail to fetch content',error)

        else:
            print(success['content_body'])

        
    
    return render_template('tutorial_dash.html',tp_check=tp_summary)


def select_topic(value):
   sql='''
   SELECT id,topic_number,content_body,topic_name
   FROM content
   WHERE id=%s;
'''      

   conn = None
   try:
       conn = db_pool.getconn()
       with conn.cursor(cursor_factory=RealDictCursor) as cur:
               cur.execute(sql, (value,))
               row = cur.fetchone()
       return row, None
   except Exception as e:
           if conn:
               conn.rollback()
           if conn and isinstance(e, (psycopg2.OperationalError, psycopg2.InterfaceError)):
               conn.close()
               conn = None
           return None, str(e)
   finally:
           if conn:
               db_pool.putconn(conn)


def tp_sum():#this is summary for topic dashaboard
   sql='''
   SELECT id,topic_number,topic_name
   FROM content;
''' 

   conn = None
   try:
          conn = db_pool.getconn()
          with conn.cursor(cursor_factory=RealDictCursor) as cur:
                  cur.execute(sql)
                  row = cur.fetchall()
          return row, None
   except Exception as e:
              if conn:
                  conn.rollback()
              if conn and isinstance(e, (psycopg2.OperationalError, psycopg2.InterfaceError)):
                  conn.close()
                  conn = None
              return None, str(e)
   finally:
              if conn:
                  db_pool.putconn(conn)

   


@app.route('/topic/<int:topic_id>') 
def tuto_home(topic_id):

    success, error = select_topic(topic_id)
    
    if not success:
        return "Topic not found", 404
        print(error)


    return render_template('tutorial_home.html', content_data=success)

if __name__=='__main__':
    app.run(debug=True, use_reloader=True)


=======
# This codes where written by me hussein martin nkya from 24/8/2026
# I pray to God that this project to impact thousands of students in Tanzania and Africa in large

from flask import Flask ,request,redirect,url_for,session,render_template
import atexit
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL')
SECRET_KEY=os.getenv('SECRET_KEY')

# Global connection pool initialization
db_pool = ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DATABASE_URL,
    sslmode="require")
    
# Automatically close all pooled connections when app stops
@atexit.register
def close_db_pool():
    if db_pool:
        db_pool.closeall()


app = Flask(__name__)
app.secret_key=SECRET_KEY

# i ended here for today so we will start from tomorrow
@app.route('/login',methods=['POST','GET'])
def sign_in():
    if request.method=='POST':
        action=request.form.get('action')

        if action=='login':
            pass

    return render_template('login.html')

def user_login():
    sql='''
    
'''

@app.route('/new_content',methods=['POST','GET'])
def create_content():
    if request.method=='POST':
        topic_number=request.form.get('topic_no')
        topic_name=request.form.get('topic_name')
        topic_body=request.form.get('content')
        topic_example=request.form.get('example')

        values=[topic_number,topic_name,topic_body,topic_example]

        success,error=insert_content(values)

        if not success:
            print('error:',error)
        else:
            print('successfull content added')

    
    return render_template('create_content.html')
def insert_content(values):
    sql='''
    INSERT INTO content(topic_number,topic_name,content_body,example)
    VALUES(%s,%s,%s,%s)
'''

    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(sql, values)
        conn.commit()
        return True, None
    except Exception as e:
        if conn:
            conn.rollback()
        return False, str(e)
    finally:
        if conn:
            db_pool.putconn(conn)
    
def topic_select():
    sql='''
    SELECT topic_number,topic_name 
    FROM content
'''
    conn=None
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return rows, None
    except Exception as e:
        if conn:
            conn.rollback()
        return [], str(e)
    finally:
        if conn:
            db_pool.putconn(conn)

@app.route('/new_eg',methods=['POST','GET'])
def create_eg():
    if request.method=='POST':
        topic=request.form.get('topic')
        name=request.form.get('eg_name')
        country=request.form.get('country')
        apply_to=request.form.get('apply_to')
        skills=request.form.get('apply_to')
        achieve=request.form.get('achieve')
        avatar=request.form.get('avatar')
        question=request.form.get('question')
        response=request.form.get('response')
        word_count=request.form.get('word_count')
        eg_no=request.form.get('eg_no')
        comment=request.form.get('comment')

        values=[name,country,apply_to,skills,achieve,avatar,question,response,eg_no,comment,topic,word_count]
        success,error=new_example(values)

        if not success:
            print('ERROR',error)
        else:
            print('successfull example added')

    list_topic,error=topic_select()

    if not list_topic:
        print('ERROR',error)


    return render_template('create_eg.html',topic_list=list_topic)


def new_example(values):
    sql='''
  INSERT INTO example(name,country,college,skills,achieves,avatar,question,response,example_no,comment,topic_id,word_count)
  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
'''
    
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(sql, values)
        conn.commit()
        return True, None
    except Exception as e:
        if conn:
            conn.rollback()
        return False, str(e)
    finally:
        if conn:
            db_pool.putconn(conn)

@app.route('/edit_content',methods=['POST','GET'])
def content_edit():
     
    search=[]
    error=None
    get_content=[]

    search,error=topic_select()

    if not search:
           print('fail to load names',error)

    if request.method=='POST':

        action=request.form.get('action')

        if action=='search_by_name':
            name=request.form.get('topic_name')

            get_content,error=name_search_content(name)

            if not get_content:
               print('ERROR',error)

        if action=='update_from_name':
            topic_name=request.form.get('topic_name')
            topic_number=request.form.get('topic_number')
            content_body=request.form.get('body')
            example=request.form.get('example')
            content_id=request.form.get('content_id')

            success,error=update_content(topic_name,topic_number,content_body,example,content_id)

            if not success:
                print('FAIL TO UPDATE',error)
 
    return render_template('edit_content.html',search_name=search,content=get_content)


def name_search_content(name):
    sql='''
   SELECT topic_number,topic_name,content_body,example,id
   FROM content
   WHERE topic_name=%s;
'''

    conn = None
   
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql,(name,))
                row=cur.fetchone()
        
        return row,None
    except Exception as e:
        if conn:
            conn.rollback()
        return [], str(e)
    finally:
        if conn:
            db_pool.putconn(conn)

def update_content(topic_number,topic_name,content_body,example,content_id):
    sql='''
    UPDATE content 
    SET topic_number = %s, topic_name = %s, content_body = %s ,example=%s
    WHERE id = %s 
    RETURNING topic_number, topic_name, content_body,example,id;
'''
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql,(topic_name,topic_number,content_body,example,content_id))
            row=cur.fetchone()
            
        conn.commit()   
        return row,None
    except Exception as e:
            if conn:
                conn.rollback()
            return [], str(e)
    finally:
            if conn:
                db_pool.putconn(conn)


@app.route('/update_example',methods=['POST','GET'])
def edit_update():
    search=[]
    success={}
    error=None

    search,error=topic_select()
    
    if not search:
        print('fail to load topics',error)

    if request.method=='POST':
        action=request.form.get('action')

        if action=='search_example':
            name=request.form.get('topic_name')
            example=request.form.get('example_number')

            success,error=content_example(name,example)

            if not success:
                 print('Fail to access the value')



    return render_template('edit_example.html',eg_name=search,eg_value=success)

def content_example(topic_id,example_no):
    sql='''
    SELECT name,country,college,skills,achieves,avatar,question,response,example_no,comment,topic_id,word_count
    FROM example
    WHERE topic_id=%s AND example_no=%s;
    
'''        
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (topic_id,example_no))
            row = cur.fetchone()
        return row, None
    except Exception as e:
        if conn:
            conn.rollback()
        if conn and isinstance(e, (psycopg2.OperationalError, psycopg2.InterfaceError)):
            conn.close()
            conn = None
        return None, str(e)
    finally:
        if conn:
            db_pool.putconn(conn)
    
        
def edit_example(name,country,college,skills,achieves,avatar,question,response,comment,word_count,topic_id,example_no):
    sql='''
    UPDATE example
    SET name = %s ,country = %s,college = %s,skills = %s,achieves = %s,avatar = %s,question = %s,response = %s,example_no = %s,comment = %s,topic_id = %s,word_count = %s
    WHERE  topic_id = %s AND example_no = %s;
'''
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(sql, (name, country, college, skills, achieves, avatar,
                               question, response, example_no, comment, topic_id, word_count,
                               topic_id, example_no))
        conn.commit()
        return True, None
    except Exception as e:
        if conn:
            conn.rollback()
        if isinstance(e, (psycopg2.OperationalError, psycopg2.InterfaceError)):
            conn.close()
            conn = None
        return False, str(e)
    finally:
        if conn:
            db_pool.putconn(conn)



@app.route('/tuto_dash',methods=['POST','GET'])
def tdash():
    
    
    tp_summary,error=tp_sum()
    if not tp_summary:
        print('Fail to analyze topic',error)

    success=None
    if request.method=='POST':
        tp_id=request.form.get('topic_ref')

        if tp_id:
            return redirect(url_for('tuto_home',topic_id=tp_id))

        success,error=select_topic(tp_id)

        if not success:
            print('fail to fetch content',error)

        else:
            print(success['content_body'])

        
    
    return render_template('tutorial_dash.html',tp_check=tp_summary)


def select_topic(value):
   sql='''
   SELECT id,topic_number,content_body,topic_name
   FROM content
   WHERE id=%s;
'''      

   conn = None
   try:
       conn = db_pool.getconn()
       with conn.cursor(cursor_factory=RealDictCursor) as cur:
               cur.execute(sql, (value,))
               row = cur.fetchone()
       return row, None
   except Exception as e:
           if conn:
               conn.rollback()
           if conn and isinstance(e, (psycopg2.OperationalError, psycopg2.InterfaceError)):
               conn.close()
               conn = None
           return None, str(e)
   finally:
           if conn:
               db_pool.putconn(conn)


def tp_sum():#this is summary for topic dashaboard
   sql='''
   SELECT id,topic_number,topic_name
   FROM content;
''' 

   conn = None
   try:
          conn = db_pool.getconn()
          with conn.cursor(cursor_factory=RealDictCursor) as cur:
                  cur.execute(sql)
                  row = cur.fetchall()
          return row, None
   except Exception as e:
              if conn:
                  conn.rollback()
              if conn and isinstance(e, (psycopg2.OperationalError, psycopg2.InterfaceError)):
                  conn.close()
                  conn = None
              return None, str(e)
   finally:
              if conn:
                  db_pool.putconn(conn)

   


@app.route('/topic/<int:topic_id>') 
def tuto_home(topic_id):

    success, error = select_topic(topic_id)
    
    if not success:
        return "Topic not found", 404
        print(error)


    return render_template('tutorial_home.html', content_data=success)

if __name__=='__main__':
    app.run(debug=True, use_reloader=True)


>>>>>>> cdc4812e5ac1c2bb0bebdae127a81d6aadf37d59
