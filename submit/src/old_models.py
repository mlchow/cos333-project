from views import app
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects.postgresql import \
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
    INTERVAL, JSON, JSONB, MACADDR, NUMERIC, OID, REAL, SMALLINT, TEXT, \
    TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
    DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk'
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    netid = db.Column(db.String(), primary_key=True)
    degree = db.Column(db.String())
    major = db.Column(db.String())
    interested_majors = db.Column(ARRAY(db.String()))
    interested_certificates = db.Column(ARRAY(db.String()))
    courses = db.Column(ARRAY(db.String()))
    num_pdfs = db.Column(db.Integer)

    def __init__(self, netid, degree, major, interested_majors, interested_certificates, num_pdfs, courses):
        self.netid = netid
        self.degree = degree
        self.major = major
        self.interested_certificates = interested_certificates
        self.interested_majors = interested_majors
        self.num_pdfs = num_pdfs
        self.courses = courses

    def __repr__(self):
        #return '<E-mail %r>' % self.email
        return '<net-id %r>' % self.netid
        return '<degree %r>' % self.degree
        return '<major %r>' % self.major
        return '<interested_degrees %r>' % self.interested_degrees
        return '<interested_certificates %r>' % self.interested_certificates
        return '<num_pdfs %r>' % self.num_pdfs
        return '<courses %r>' % self.courses

def search_users(netid):
    netid = User.query.filter_by(netid=netid).first()
    if netid is None:
        return "New user"
    else:
        return "Existing user"

def add_user(studentinfo):
    if len(studentinfo) != 5:
        return False
    netid = studentinfo[0]
    if search_users(netid) == "New user":
        degree = studentinfo[1]
        major = studentinfo[2]
        courses = studentinfo[3]
        num_pdfs = studentinfo[4]
        interested_majors = []
        interested_certificates = []
        new_user = User(netid,degree,major,interested_majors,interested_certificates,num_pdfs,courses)
        db.session.add(new_user)
        db.session.commit()
    return False

