import os
import os.path
from pathlib import Path

from flask import Flask, request

app = Flask(__name__)


CONTENT_KEY='content'

def check_student_dir(student):
    if not Path(student).is_dir():
        os.mkdir(student)

@app.route('/fexchange/<student>/<contentid>', methods=['GET'])
def retrieve(student,contentid):
    check_student_dir(student)
    fname = os.path.join(student,contentid)
    if Path(fname).is_file():
        content = ''
        with open(fname,'r') as f:
            content = f.read()
        return content
    else:
        return f'No content found for student {student} and content id {contentid}'

@app.route('/fexchange/<student>/<contentid>', methods=['POST'])
def submit(student,contentid):
    check_student_dir(student)
    data = request.form.to_dict(flat=False)
    if CONTENT_KEY in data:
        # TODO size limit
        with open(os.path.join(student,contentid),'w') as wf:
            wf.write(data[CONTENT_KEY][0])
    else:
        print(data)
        return f'Student {student} did not include content for {contentid}'
    return f'Student {student} sent content for {contentid}'
  
@app.route('/greet/<student>')
def say_hello(student):
    return f'Hello from Server to student {student}'
  
@app.route('/status')
def status():
    return 'Server running'


