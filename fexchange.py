import os
import os.path
from pathlib import Path

from flask import Flask, request

app = Flask(__name__)


CONTENT_KEY='content'

DATA_DIR='data'

MAX_CONTENT_SIZE=5000



def check_student_dir(student):
    sdir = os.path.join(DATA_DIR,student)
    if not Path(sdir).is_dir():
        os.mkdir(sdir)

@app.route('/fexchange/<student>/<contentid>', methods=['GET'])
def retrieve(student,contentid):
    check_student_dir(student)
    fname = os.path.join(DATA_DIR,student,contentid)
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
        content = data[CONTENT_KEY][0]
        if len(content) > MAX_CONTENT_SIZE:
            return f'Content longer than {MAX_CONTENT_SIZE} characters for student {student} and content {contentid}'
        with open(os.path.join(DATA_DIR,student,contentid),'w') as wf:
            wf.write(content)
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


