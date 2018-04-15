from app import db


goods = db.Table('goods',
    db.Column('good_id', db.Integer, db.ForeignKey('good.id'), primary_key=True),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id'), primary_key=True)
)

good_countries = db.Table('good_countries',
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'), primary_key=True),
    db.Column('good_id', db.Integer, db.ForeignKey('good.id'), primary_key=True)
)


class Company(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    compname = db.Column(db.String(80),  index=True, nullable=False)
    website = db.Column(db.String(120) )
    twitter_handle = db.Column(db.String(120) )
    address = db.Column(db.String(120) )
    knowthechain_score = db.Column(db.String(8))
    knowthechain_link = db.Column(db.String(120))
    transparency = db.Column(db.String(256) )
    goods = db.relationship('Good', secondary=goods, lazy='subquery',
                            backref=db.backref('companies', lazy=True))

    def __repr__(self):
        return '<Company %r>' % self.compname


class Good(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    goodname = db.Column(db.String(80), unique=True, nullable=False)
    good_countries = db.relationship('Country', secondary=good_countries, lazy='subquery',
                                     backref=db.backref('goods', lazy=True))

    def __repr__(self):
        return '<Good %r>' % self.goodname


class Country(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    countryname = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Country %r>' % self.countryname
