from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_main_script():
    subprocess.run(['python', 'main.py'])
    return 'Main script executed!'

@app.route('/face-recognition', methods=['POST'])
def run_face_recognition_script():
    subprocess.run(['python', 'tempCodeRunnerFile.py'])
    return 'Face recognition script executed!'

if __name__ == '__main__':
    app.run(debug=True)
