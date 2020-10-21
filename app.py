""" Zipvote: Tarini, Isabelle, Sarah
 this app searches through the district database to present info about members of congress/elected officials
 form gathers data from user on what they'd like to see"""
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)
import cs304dbi as dbi
import functions as f
import os
import bcrypt
import random
app.secret_key = 'welovezipvotesit'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
UPLOAD_FOLDER='politician_data_review'
ALLOWED_EXTENSIONS=set(['pdf','doc','docx'])
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

up_votes = 0
down_votes = 0

"""Routes to main.html main landing page,every other page has option to return here"""
@app.route('/')
def index():
   return render_template('main.html', title = "Home")

"""Allows user to create an account """     
@app.route('/join/', methods=["POST"])
def join():
    try:
        username = request.form['username']
        passwd1 = request.form['password1']
        passwd2 = request.form['password2']
        if passwd1 != passwd2:
            flash('Passwords do not match')
            return redirect( url_for('index'))
        hashed = bcrypt.hashpw(passwd1.encode('utf-8'), bcrypt.gensalt())
        hashed_str = hashed.decode('utf-8')
        print(passwd1, type(passwd1), hashed, hashed_str)
        conn = dbi.connect()
        curs = dbi.cursor(conn)
        try:
            curs.execute('''INSERT INTO userpass(uid,username,hashed)
                            VALUES(null,%s,%s)''',
                         [username, hashed_str])
            conn.commit()
        except Exception as err:
            flash('That username is taken: {}'.format(repr(err)))
            return redirect(url_for('index'))
        curs.execute('select last_insert_id()')
        row = curs.fetchone()
        uid = row[0]
        flash('You were issued UID {}'.format(uid))
        session['username'] = username
        session['uid'] = uid
        session['logged_in'] = True
        return redirect( url_for('user', username=username) )
    except Exception as err:
        flash('Form Submission Error '+str(err))
        return redirect( url_for('index') )
"""User can choose between logging in and creating an account """     
@app.route('/choose/', methods=["POST"])
def choose():
    if request.form.get("menu")=="Create":
        return render_template('join.html')
    elif request.form.get("menu")=="Login":
        return render_template('login.html')
    else: 
        flash('You must select an option!')
        return redirect(url_for('index'))
"""Login process, creating secure password and starting session"""
@app.route('/login',methods=["POST"])
def login():
    try:
        username = request.form['username']
        passwd = request.form['password']
        conn = dbi.connect()
        curs = dbi.dict_cursor(conn)
        curs.execute('''SELECT uid,hashed
                      FROM userpass
                      WHERE username = %s''',
                     [username])
        row = curs.fetchone()
        if row is None:
            # Same response as wrong password,
            # so no information about what went wrong
            flash('Login incorrect. Try again or create account')
            return redirect( url_for('index'))
        hashed = row['hashed']
        print('database has hashed: {} {}'.format(hashed,type(hashed)))
        print('form supplied passwd: {} {}'.format(passwd,type(passwd)))
        hashed2 = bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8'))
        hashed2_str = hashed2.decode('utf-8')
        print('rehash is: {} {}'.format(hashed2_str,type(hashed2_str)))
        if hashed2_str == hashed:
            print('Passwords match!')
            flash('Successfully logged in as '+username)
            session['username'] = username
            session['uid'] = row['uid']
            session['logged_in'] = True
            return redirect( url_for('user', username=username) )
        else:
            flash('Login incorrect. Try again or join')
            return redirect( url_for('index'))
    except Exception as err:
        flash('Form submission error '+str(err))
        return redirect( url_for('index') )
"""Notifies user once they are logged in of their UID and username"""
@app.route('/user/<username>')
def user(username):
    try:
        # don't trust the URL; 
        if 'username' in session:
            username = session['username']
            uid = session['uid']
            flash('You are now logged in as  ' + username+' and your UID is '+str(uid))
            return render_template('main.html',
                                   name=username,
                                   uid=uid)
        else:
            flash('You are not logged in. Please login or join')
            return redirect( url_for('index') )
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect( url_for('index') )

"""Allows user to add a politician to their list"""       
@app.route('/fav', methods=["GET", "POST"])
def fav():
    conn = dbi.connect()
    if 'username' in session:
        username=session['username']
        person_id=request.form.get('menu')
        person_id=int(person_id)
        f.addtolist(conn,username,person_id)
        flash('Successfully added politician to your list')
    return redirect(url_for('userpage'))

"""Allows user to update stance on a politician or delete politician from list"""
@app.route('/update/<person_id>',methods=["GET","POST"])
def update(person_id):
    conn = dbi.connect()
    if 'username' in session:
        username=session['username']
        if request.form.get('submit')=="choose":
            username=session['username']
            feelings=request.form.get('menu')
            f.update(conn,feelings,username,person_id)
            flash('Updated stance successfully')
        elif request.form.get('submit')=="delete":
            print('delete')
            flash('Politician deleted from your list successfully.')
            f.delete(conn,person_id,username)
    return redirect(url_for('userpage'))

@app.route('/updateAjax/<person_id>', methods=['POST'])
def updateAjax():
    conn = dbi.connect()
    feelings = request.form.get('feelings')
    person_id = request.form.get('person_id')

    if 'username' in session:
        uid = session['uid']
        f.update(conn,feelings,uid,person_id)

        return jsonify({'error': False, 'person_id':person_id, 'feelings': feelings})
    else:
        return jsonify({'error': True, 'err':"Please log in"})

"""Displays page with users bookmarked politicians"""
@app.route('/userpage')
def userpage():
    conn = dbi.connect()
    polist=f.polist(conn)
    try:
        # don't trust the URL; 
        if 'username' in session:
            username = session['username']
            uid = session['uid']
            userlist=f.userfavs(conn,username)
            return render_template('userpage.html',
                                   name=username,
                                   uid=uid,userlist=userlist,polist=polist)
        else:
            flash('You are not logged in. Please login or join to access your page.')
            return redirect( url_for('index') )
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect( url_for('index') )

@app.route('/logout/')
def logout():
    try:
        if 'username' in session:
            username = session['username']
            session.pop('username')
            session.pop('uid')
            session.pop('logged_in')
            flash('You are logged out')
            return redirect(url_for('index'))
        else:
            flash('You are not logged in. Please login or join')
            return redirect( url_for('index') )
    except Exception as err:
        flash('Some kind of error '+str(err))
        return redirect( url_for('index') )

"""Renders template about which has a  summary on our motivations and group ideologies"""   
@app.route('/about/')
def aboutus():

    return render_template('about.html')

@app.route('/updateAbout/',methods=["GET","POST"])
def updateAbout2() :
    global up_votes, down_votes
    data = request.form
    if data.get('up'):
        up_votes += 1
    elif data.get('down'):
        down_votes += 1
    else:
        # could probably do some sort of error, but let's just leave
        # the counters alone. the handler will return the current values
        pass
    # response dictionary
    resp_dic = {'up': up_votes, 'down': down_votes}
    return jsonify(resp_dic)

"""check if file is in allowed format"""
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/mainupload',methods=['POST'])
def mainupload():
    conn=dbi.connect()
    return render_template('upload.html',polist=f.polist(conn))  


"""once user uploads their file, it will request through form and save"""
@app.route('/uploader',methods=['POST'])
def uploading():
    """If theres not, notify user to log in"""
    conn=dbi.connect()
    if 'username' not in session:
        flash("You need to login to upload a file.")
        return render_template('upload.html')
    else:
        if 'file' not in request.files:
            flash('No file part')
        file=request.files['file']
        if file.filename=='':
            flash('No selected file')
        if file and allowed_file(file.filename):
            person_id=request.form.get('submit')
            filename=secure_filename(file.filename)
            filename=filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            flash(filename+'Successfully Uploaded! We will review and get back to you')
        else:
            flash('Incorrect format. Submit pdf or docx only.')
    return render_template('upload.html',polist=f.polist(conn))        


""" try:
            f=request.files['file']
            filename=secure_filename(f.filename)
            if filename!='':
                file_ext=os.path.splittext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    abort(400)
                    f.save(os.path.join(app.config['UPLOAD_PATH'],filename))
                    flash('File uploaded sucessfully. We will review and update accordingly!')
return render_template('upload.html')"""
    
"""routes to search page, allowing person to fill in info on candidate"""
@app.route('/results/', methods=["GET", "POST"]) 
def results():
    conn = dbi.connect()
    if request.method=='POST':
        if 'Zipcode!' in request.form.values():
            searched=request.form['search-zipcode']
            ziplist=f.ziplist(searched,conn)
            if len(ziplist)==0:
                """routes to notfound page"""
                return render_template('not_found.html',searched=searched)
            elif len(ziplist)==1:
                for zipcode in ziplist:
                    zipcode=zipcode['zipcode']
                return redirect(url_for('zipcode',zipcode=zipcode))
            else:
                return render_template('zipresults.html',ziplist=ziplist,searched=searched,type=zipcode)
        elif 'Name!' in request.form.values():
            searched=request.form['search-name']
            plist=f.plist(searched,conn)
            if (len(plist)==0):
                    return render_template('not_found.html',searched=searched,type=politician)
            elif len(plist)==1:
                for person in plist:
                    person_id=person['person_id']
                    return redirect(url_for('politician',person_id=person_id))
            else:
                return render_template('results.html',plist=plist,searched=searched,type=politician)
        else:
             """ 'Upload!' in request.form.values():"""
             return render_template('upload.html')


"""zipcode will gather information on a zipcode given the zip # and render it through the zipcode template """
@app.route('/zipcode/<zipcode>')
def zipcode(zipcode):
    conn = dbi.connect()
    politicianNames = f.politiciansforarea(zipcode,conn)
    info = f.zipcodeinfo(zipcode, conn)
    return render_template('zipcode.html', zinfo = info, politician = politicianNames)

"""politician will gather information on a politician given a politician # and render it through politician template"""
@app.route('/politician/<person_id>')
def politician(person_id):
    conn = dbi.connect()
    info = f.pidinfo(person_id, conn)
    info = f.addpos(info,conn)
    pid=person_id
    policies=f.policies(pid,conn)
    return render_template('politician.html', pinfo = info,policies=policies)

@app.route('/office/<int:num>')
def office(num):
    conn = dbi.connect()
    info = f.oidinfo(num, conn)
    return render_template('office.html', oinfo = info)

@app.before_first_request
def startup():
   dbi.cache_cnf()
   dbi.use('zipvote_db')

if __name__ == '__main__':
    # dbi.cache_cnf()
    # dbi.use('zipdb')
    # conn=dbi.connect()
    # app.run(debug=True)
    import sys, os
    uid=os.getuid()
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0', port)
