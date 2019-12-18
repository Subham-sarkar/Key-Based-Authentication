"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import os
from flask import Flask, jsonify, make_response, render_template, flash, request, redirect, url_for
import jwt
import datetime
from functools import wraps
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} #only images
app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# function to check the validity
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')

        if not token:
            return jsonify({'messaage' : 'Token is missing!'}), 403
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])

        except:
            return jsonify({'message' : 'Token is invalid'}), 403

        return f(*args, **kwargs)

    return decorated

# testing the valid token
@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this!!!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'This is only available for people with valid tokens!!!'})


#UPLOAD API
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods = ["GET", "POST"])
@token_required
def hello():
    if request.method=="POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file=request.files["file"]
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)    
            file.save(os.path.join("uploads", file.filename))
            return render_template("page2.html", name=file.filename)
    return render_template("index.html", message="Upload")


@app.route('/')
def login():
    
        t = request.cookies.get('token');
        if not t:  
            auth = request.authorization
            if auth and auth.password == 'secret':
                token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, app.config['SECRET_KEY'])
                resp = make_response(redirect('/upload'));
                resp.set_cookie('token', token);
                return resp
            return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

        else:
            try:
                data = jwt.decode(t, app.config['SECRET_KEY'])
                return redirect('http://localhost:5555/upload')
            except: 
                auth = request.authorization
                if auth and auth.password == 'secret':
                    token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, app.config['SECRET_KEY'])
                    resp = make_response(redirect('/upload'));
                    resp.set_cookie('token', token);
                    return resp
                return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})



if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.debug = True    
    app.run(HOST, PORT)
