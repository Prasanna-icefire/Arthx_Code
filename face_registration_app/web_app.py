from flask import Flask, Response, render_template, request, redirect, url_for
from register_face import *
from faster_recognition import *
entered_name = ''
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/face_registration', methods=['POST'])
def process():
    global entered_name
    entered_name = request.form.get('name')
    return Response(start_registration(entered_name),
                    mimetype='multipart/x-mixed-replace; boundary=frame')    

if __name__ == '__main__':
    app.run(debug=True, host='discpi.local')