from flask import Flask, render_template  #

app = Flask(__name__)
my_tasks = ['Learn Flask', 'Create App']

@app.route('/', methods=['GET', 'POST'])    #
def index():
    if request.method == 'POST':            #
        new_task = request.form['content']  #
        my_tasks.append(new_task)           #
        return redirect('/')                #
    else:
        return render_template('index.html', tasks=my_tasks)