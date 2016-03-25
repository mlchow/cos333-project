from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/my_studentdb2'
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    netid = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120), unique=True)
    degree = db.Column(db.String(400))
    interested_degree = db.Column(db.String(40))
    interested_certificates = db.Column(db.String(40))
    num_pdfs = db.Column(db.Integer)

    def __init__(self, netid, email, degree, interested_degree, interested_certificates, num_pdfs):
        self.netid = netid
        self.email = email
        self.degree = degree
        self.interested_certificates = interested_certificates
        self.interested_degree = interested_degree
        self.num_pdfs = num_pdfs

    def __repr__(self):
        return '<E-mail %r>' % self.email
        return '<net-id %r>' % self.netid
        return '<degree %r>' % self.degree
        return '<interested_degree %r>' % self.interested_degree
        return '<interested_certificates %r>' % self.interested_certificates
        return '<num_pdfs %r>' % self.num_pdfs

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        netid = request.form['netid']
        degree = request.form['degree']
        interested_degree = request.form['interested_degree']
        interested_certificates = request.form['interested_certificates']
        num_pdfs = request.form['pdf']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.netid == netid).count():
            reg = User(netid, email, degree, interested_degree, interested_certificates, num_pdfs)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()