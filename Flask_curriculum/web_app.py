from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/finger_register', methods=['POST'])
def finger_register():
    print("Button was pressed!")
    #Start Finger Print Registration Process here
    return "Script executed"

@app.route('/face_register', methods=['POST'])
def face_register():
    print("Button was pressed!")
    #Start Finger Print Registration Process here
    return "Script executed"

@app.route('/finger_scan', methods=['POST'])
def finger_scan():
    print("Button was pressed!")
    #Start Finger Print Registration Process here
    return "Script executed"

@app.route('/face_scan', methods=['POST'])
def face_scan():
    print("Button was pressed!")
    #Start Finger Print Registration Process here
    return "Script executed"

if __name__ == '__main__':
    app.run(debug=True)
