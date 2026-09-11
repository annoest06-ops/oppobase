# This codes where written by me hussein martin nkya from 24/8/2026
# I pray to God that this project to impact thousands of students in Tanzania and Africa in large

from flask import Flask ,request,redirect,url_for,session,render_template
import atexit
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from engine import analysis_prompt #this function is for ai calling from another py file

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

@app.route('/login', methods=['POST', 'GET'])
def sign_in():

    message = None  # only set this when there's actually something to report

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('passcode')

        user, error = user_login(username, password)

        if error:
            print('Database Error:', error)
            message = 'Something went wrong. Please try again.'
            return render_template('login.html', message=message)

        if user and user['username'] == username and user['password'] == password:
            session['username'] = username
            if username == 'admin':
                return redirect(url_for('admin_dash'))
            
            elif username == 'student':
                return redirect(url_for('new'))
            
            else:
                return redirect(url_for('user_dash'))

        else:
            message = 'Invalid username or password. Please try again.'
            return render_template('login.html', message=message)

    return render_template('login.html', message=message)

def user_login(username,password):
    # Parameterized query to prevent SQL Injection
    sql = '''
        SELECT username, password
        FROM account
        WHERE username = %s AND password = %s
    '''
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (username,password))
            user = cur.fetchone()  # Returns None if no user is found
        return user, None
    except Exception as e:
        if conn:
            conn.rollback()
        return None, str(e)
    finally:
        if conn:
            db_pool.putconn(conn)


@app.route('/userdash', methods=['POST', 'GET'])
def user_dash():
    if 'username' not in session:
        return redirect(url_for('sign_in'))

    username = session['username']
    
    
    return render_template('user_dash.html', username=username)

@app.route('/admindash',methods=['POST','GET'])
def admin_dash():
    if 'username' not in session:
        return redirect(url_for('sign_in'))

    username = session['username']
    return render_template('admin_dash.html', username=username)


@app.route('/new_content',methods=['POST','GET'])
def create_content():

    if 'username' not in session:
            return redirect(url_for('sign_in'))
    
    if request.method=='POST':
        topic_number=request.form.get('topic_no')
        topic_name=request.form.get('topic_name')
        topic_body=request.form.get('content')
        topic_example=request.form.get('example')

        values=[topic_number,topic_name,topic_body,topic_example]

        success,error=insert_content(values)

        if not success:
           print('error:',error)
           return render_template('create_content.html', message='Error adding content')
            
     
    
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

    if 'username' not in session:
            return redirect(url_for('sign_in'))
    
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

    if 'username' not in session:
            return redirect(url_for('sign_in'))
    
     
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

    if 'username' not in session:
            return redirect(url_for('sign_in'))

    
    search=[]
    success=[]
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

    if 'username' not in session:
            return redirect(url_for('sign_in'))
    
    
    
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

   


@app.route('/tutorial_view') 
def tuto_home():

    if 'username' not in session:
            return redirect(url_for('sign_in'))

    topic_id=request.args.get('topic_id')
    

    success, error = select_topic(topic_id)
    
    if not success:
        return "Topic not found", 404
        print(error)


    return render_template('tutorial_view.html', content_data=success)


@app.route('/myboard',methods=['POST','GET'])
def my_board():

    if 'username' not in session:
            return redirect(url_for('sign_in'))

    user=session.get('username')
    if request.method=='POST':
         date=request.form.get('date')
         subject=request.form.get('subject')
         content=request.form.get('content')
         username=request.form.get('user_id')

         values=[date,subject,content,user]
         success,error=board(values)
         message='Fail to add content to board'

         if not success:
            print('ERROR',error)
            return render_template('myboard.html',message=message)

         user=session.get('username')   
        

    return render_template('myboard.html',user_id=user)


def board(values):
    sql='''
  INSERT INTO myboard(date,subject,content,username)   
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


@app.route('/reference',methods=['POST','GET'])
def create_ref():

    if 'username' not in session:
            return redirect(url_for('sign_in'))
    

    if request.method=='POST':
        name=request.form.get('ref_quest')
        response=request.form.get('ref_response')
        comment=request.form.get('ref_comment')

        values=[name,response,comment]

        success,error=new_ref(values)

        if not success:
             print('ERROR',error)

    return render_template('reference.html')

def new_ref(values):
    sql='''
   INSERT INTO reference(question,body,comment)
   VALUES(%s,%s,%s)
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
    


@app.route('/scholarship',methods=['POST','GET'])
def scholar():

    if 'username' not in session:
            return redirect(url_for('sign_in'))
    

    if request.method=='POST':
        name=request.form.get('title')
        deadline=request.form.get('deadline')
        location=request.form.get('location')
        about=request.form.get('about')
        comment=request.form.get('comment')

        values=[name,deadline,location,about,comment]

        success,error=create_scholar(values)

        if not success:
            print('ERROR',error)
            return render_template('scholarship.html',message='Fail to add scholarship')

    return render_template('scholarship.html')


def create_scholar(values):
    sql='''
    INSERT INTO scholarship(title,deadline,location,content,comment)
    VALUES(%s,%s,%s,%s,%s)
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


@app.route('/question',methods=['POST','GET'])
def quest():

    if 'username' not in session:
            return redirect(url_for('sign_in'))
    

    title,bad=scholar()

    if not title:
        print('ERROR',bad)

    if request.method=='POST':
        scholar_name=request.form.get('ship_name')
        number=request.form.get('qn_number')
        question=request.form.get('question')
        word_count=request.form.get('word_count')

        values=[question,scholar_name,word_count,number]

        success,error=new_quest(values)

        if not success:
            print('ERROR',error)
            message='Fail to add question'
            return render_template('question.html',message=message)

    return render_template('question.html' , names=title)

def new_quest(values):
    sql='''
    INSERT INTO question(question,scholar_id,word_count,number)
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



def scholar():
    #this is the function for scholarship name used in selection list

    sql="""
   SELECT  title,scholar_id
   FROM scholarship
   """

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

    

@app.route('/schol_dash', methods=['POST', 'GET'])
def schol_dash():

    if 'username' not in session:
            return redirect(url_for('sign_in'))
    

    schol_summary, error = schol_sum()
    if not schol_summary:
        print('Failed to fetch scholarships:', error)

    if request.method == 'POST':
        schol_id = request.form.get('schol_id')
        print('scholarship id:',schol_id)

        if schol_id:
            return redirect(url_for('schol_detail', schol_name=schol_id))

    return render_template('scholarship_dash.html', schol_summary=schol_summary)


def schol_sum():
    sql='''
     SELECT scholar_id ,title,deadline,location
     FROM scholarship
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


@app.route('/scholar_detail', methods=['GET','POST'])
def schol_detail():

    if 'username' not in session:
            return redirect(url_for('sign_in'))
    

    if request.method=='POST':
        data_id=request.form.get('data_id')

        if data_id:
          return redirect(url_for('quest_dash',data_id=data_id))

    schol_name=request.args.get('schol_name')
    
        
    schol, error = select_scholarship(schol_name)
    
    if not schol:
        print('Failed to fetch scholarship:i think is here', error)
     


    return render_template('scholarship_detail.html', schol=schol,scholar_id=schol_name)

def select_scholarship(value):
   sql='''
   SELECT title,content,comment,scholar_id
   FROM 
   scholarship
   WHERE scholar_id=%s
'''

   conn = None
   try:
                 conn = db_pool.getconn()
                 with conn.cursor(cursor_factory=RealDictCursor) as cur:
                         cur.execute(sql,(value,))
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


def select_question(scholar_id):
    sql='''
    SELECT number,question
    FROM question
    WHERE scholar_id=%s
'''

    conn = None
    try:
                     conn = db_pool.getconn()
                     with conn.cursor(cursor_factory=RealDictCursor) as cur:
                             cur.execute(sql,(scholar_id,))
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
    
@app.route('/question_dash', methods=['POST', 'GET'])
def quest_dash():

    if 'username' not in session:
            return redirect(url_for('sign_in'))
    
    scholarship_id = request.args.get('data_id')
  
    data, error = select_question(scholarship_id)

    if not data:
        print('error fetch question', error)

    if request.method == 'POST':
        scholar_id= request.form.get('scholarship_id')
        question_number = request.form.get('question_number')


        if question_number and scholar_id:
            return redirect(url_for('quest_view', question_no=question_number, scholar_id=scholar_id))

    return render_template('question_dash.html', data=data, scholarship_id=scholarship_id)



def view_data(scholarship_id,question_number):
    sql = """
        SELECT number,question,scholar_id
        FROM question
        WHERE scholar_id = %s AND number = %s
    """
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (scholarship_id, question_number))
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


@app.route('/question_view',methods=['POST','GET'])
def quest_view():

    if 'username' not in session:
        return redirect(url_for('sign_in'))
    

    question_no = request.args.get('question_no')
    scholarship_id = request.args.get('scholar_id')
    
    fetch_data, error = view_data(scholarship_id, question_no)

    if not fetch_data:
        print('error fetch question', error)

    user=session.get('username')

   
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'understand':
        
            number=request.form.get('question_no')
            question=request.form.get('question')
            scholar_id=request.form.get('scholarship_id')

            achieves,opps=achievements(user)
            refs,error=reference()
            #question
            personal_info,fails=personal_details(user)

            instruction_prompt=f"""
You are a scholarship application coach for a high school student. Your job is to GUIDE, never to write their essay for them.

CONTEXT ON YOUR STUDENTS:
You are coaching Tanzanian students, many from hard economic backgrounds, who are working hard to excel academically and bring meaningful impact to their communities. For many of them, a scholarship isn't just an opportunity — it's a path to helping their family move out of poverty. Many have already shown this drive through community projects, initiatives, and hands-on involvement in their local area. Keep this context in mind to coach with genuine respect and encouragement — but never assume or insert these details into a specific student's answer unless their own data actually supports it. Let their real story lead, not a generic narrative.

STUDENT DATA:

Personal details: full name, date of birth, career path, school, subject combination, courses — {personal_info}

Achievements: {achieves}

SCHOLARSHIP QUESTION:
"{question}"

REFERENCE ESSAYS (past essays flagged as strong by the scholarship department):
{refs}

IMPORTANT ON REFERENCE ESSAYS:

Use these ONLY to detect structural patterns (e.g. "strong answers show a clear turning point" or "strong answers name a specific person affected").
NEVER quote, paraphrase, or borrow specific words, phrases, or content from them.
NEVER mention the reference essays exist to the student — the guidance should feel personal, not templated.

PERSONALIZATION:
Open by addressing the student by their first name (pulled from their personal details) so they immediately feel seen and supported — not a generic greeting, something that feels like a coach who actually knows them.

YOUR TASK:

Decode what this question is really testing, in 2-3 plain-language sentences (no jargon) — enough to help them understand not just *what* it's asking but *why* the scholarship committee cares about this answer.
Silently compare the question against the pattern found in reference essays to sharpen your understanding of what makes a strong answer here.
Suggest 1-2 SPECIFIC achievements from the student's data that fit this question best, and say why in one or two lines each. Only bring in themes of hardship, family impact, or community involvement if the student's own achievements or personal details genuinely reflect that — don't force it.
End with ONE concrete next step: a specific question about a single moment, or a small task like "write 3 sentences about X." It must reference something from their own achievements/data — never generic. The student should know exactly what to do next after reading it, in one glance.

RULES:

Never write example sentences or draft text for the essay itself.
Never use complex scholarship jargon — this student is new to applications.
Keep the whole response between 220 and 320 words — enough room to feel personal and complete, without dragging.
Use short sections with emojis as headers. Leave a blank line between every section and between separate points within a section — never write dense, back-to-back paragraphs.
Tone: encouraging, like a coach who believes in them — not corporate or robotic.

FORMAT YOUR OUTPUT EXACTLY LIKE THIS (keep the blank lines between sections exactly as shown):

Hey [First Name] 👋

🎯 What they're really asking:
[2-3 sentences]

💡 Your best material:
[Achievement name] — [why it fits, 1-2 lines]

[Optional 2nd achievement] — [why it fits, 1-2 lines]

✅ Try this next:
[One concrete question or micro-task, tied to a specific achievement — plain language, no hype]
"""

        question_prompt=analysis_prompt(achieves,refs,question,personal_info,instruction_prompt)
            
        if question_prompt:
            return render_template('question_view.html',question_prompt=question_prompt, question_no=number,question=question,view=fetch_data)

           
    return render_template('question_view.html', view=fetch_data)


def achievements(user):
    sql="""
    SELECT subject,content 
    FROM myboard
    WHERE username=%s
    """

    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (user,))
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

def reference():
    sql="""
    SELECT question,body,comment 
    FROM reference
    """

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

def personal_details(user):
    sql="""
    SELECT full_name,date_birth,career_path,school,combination,courses
    FROM account
    WHERE username=%s
    """

    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (user,))
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

@app.route('/new_user',methods=['POST','GET'])
def new():
    if request.method=='POST':
        fullname=request.form.get('full_name')
        datebirth=request.form.get('date_birth')
        school_name=request.form.get('school')
        comb=request.form.get('combination')
        career=request.form.get('career_path')
        courses=request.form.get('courses')
        username=request.form.get('username')
        password=request.form.get('password')

        success,error=create_new(fullname,datebirth,school_name,comb,career,courses,username,password)

        if not success:
            print('error',error)
            message='fail to save information'
            return render_template('new_user.html',message=message)

    return render_template('new_user.html')


def create_new(full_name,date_birth,school,combination,career_path,courses,username,password):
    sql="""
   INSERT INTO account(full_name,date_birth,school,combination,career_path,courses,username,password)
   VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
"""


    conn = None
    try:
            conn = db_pool.getconn()
            with conn.cursor() as cur:
                cur.execute(sql, (full_name,date_birth,school,combination,career_path,courses,username,password))
            conn.commit()
            return True, None
    except Exception as e:
            if conn:
                conn.rollback()
            return False, str(e)
    finally:
            if conn:
                db_pool.putconn(conn)

@app.route('/manage_account',methods=['POST','GET'])
def manage():
    username=session.get('username')

    view,error=pull_account(username)

    if not view:
        print('fail to fetch account info',error)

    if request.method=='POST':
        comb=request.form.get('combination')
        career_path=request.form.get('career_path')
        courses=request.form.get('courses')
        password=request.form.get('password')

        refresh,opps=update_account(comb,career_path,courses,password,username)
        message="fail to update information"
        if not refresh:
            print('fail to update account',opps)
            return render_template('account.html',view=view,message=message)

    return render_template('account.html',view=view)

def pull_account(user):
    sql="""
    SELECT combination,career_path,courses,password
    FROM account
    WHERE username=%s
    """

    conn = None
    try:
            conn = db_pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, (user,))
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

def update_account(combination,career_path,courses,password,username):
    sql="""
    UPDATE account
    SET combination=%s,career_path=%s,courses=%s,password=%s
    WHERE username=%s
    """

    conn = None
    try:
            conn = db_pool.getconn()
            with conn.cursor() as cur:
                cur.execute(sql, (combination,career_path,courses,password,username))
            conn.commit()
            return True, None
    except Exception as e:
            if conn:
                conn.rollback()
            return False, str(e)
    finally:
            if conn:
                db_pool.putconn(conn)

@app.route('/logout')
def logout_route():
    session.clear()
    return redirect(url_for('sign_in'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)