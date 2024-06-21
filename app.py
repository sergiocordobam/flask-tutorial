from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:flaskpassword@mysql/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class CDT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initial_amount = db.Column(db.Float, nullable=False)
    annual_interest_rate = db.Column(db.Float, nullable=False)
    years = db.Column(db.Integer, nullable=False)
    compounding_frequency = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=True)
    profit = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"CDT('{self.initial_amount}', '{self.annual_interest_rate}', '{self.years}', '{self.compounding_frequency}', '{self.total_amount}', '{self.profit}')"

with app.app_context():
    db.create_all()

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

            new_cdt = CDT(initial_amount=initial_amount, annual_interest_rate=annual_interest_rate, years=years, compounding_frequency=compounding_frequency, total_amount=total_amount, profit=profit)
            db.session.add(new_cdt)
            db.session.commit()

            return render_template('response_cdt.html', total_amount=total_amount, profit=profit)
    if request.method == 'GET':
        return render_template('cdt.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)