from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/<name>")
def name(name):
    return f"Hello {name}"

@app.route('/square', methods=['GET'])
def squarenumber():
    if request.method == 'GET':
        if(request.args.get('num') == None):
            return render_template('form.html')
        elif(request.args.get('num') == ''):
            return render_template('invalid_number.html')
        else:
            number = request.args.get('num')
            sq = int(number) * int(number)
            return render_template('response.html', square_of_num=sq, num=number)