from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/guest/<guest>")
def guest(guest):
    return render_template('guest.html', name=guest)

@app.route("/user/<name>", methods=['GET', 'POST'])
def user(name):
    if request.method == 'POST':
        if request.form['name'] == "":
            return render_template('invalid_user.html')
        else:
            name = request.form['name']
            if name == "admin":
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('guest', guest=name))
    if request.method == 'GET':
        return render_template('user.html')

@app.route('/square', methods=['GET', 'POST'])
def squarenumber():
    if request.method == 'POST':
        if request.form['num'] == '':
            return render_template('invalid_number.html')
        else:
            number = request.form['num']
            sq = int(number) * int(number)
            return render_template('response.html', square_of_num=sq, num=number)
    if request.method == 'GET':
        return render_template('form.html')

@app.route("/cdt", methods=['GET', 'POST'])
def cdt():
    if request.method == 'POST':
        if request.form['initial_amount'] == '' or request.form['annual_interest_rate'] == '' or request.form['years'] == '' or request.form['compounding_frequency'] == '':         
            return render_template('invalid_cdt.html')
        else:
            initial_amount = float(request.form['initial_amount'])
            annual_interest_rate = float(request.form['annual_interest_rate'])
            years = int(request.form['years'])
            compounding_frequency = int(request.form['compounding_frequency'])

            rate = annual_interest_rate / 100
            total_amount = initial_amount * (1 + rate / compounding_frequency) ** (compounding_frequency * years)
            profit = total_amount - initial_amount

            return render_template('response_cdt.html', total_amount=total_amount, profit=profit)
    if request.method == 'GET':
        return render_template('cdt.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)