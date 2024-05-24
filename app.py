from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/<name>")
def name(name):
    return f"Hello {name}"

@app.route('/square', methods=['GET', 'POST'])
def squarenumber():
    if request.method == 'POST':
        if(request.form['num'] == ''):
            return render_template('invalid_number.html')
        else:
            number = request.form['num']
            sq = int(number) * int(number)
            return render_template('response.html', square_of_num=sq, num=number)
    if request.method == 'GET':
        return render_template('form.html')
    
if __name__ == "__main__":
    app.run()