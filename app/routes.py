import os
import pandas as pd
from flask import render_template, json, request #, flash, redirect, url_for
from app import app, db
from app.models import Company, Good, Country
from custom_tweet import construct_tweet_link
import elementary 
from web_content import ibm_query_to_html
import random
import json
import pandas as pd

@app.route('/')
@app.route('/index')
def index():
    # Pull down the company info.
    comp_name = request.args.get('compname')
    product_name = request.args.get('productname')

    # Populate company info.
    company = db.session.query(Company).filter_by(compname=comp_name).first()

    # Redirection Error or no company given (aka landing page).
    if company is None or comp_name is None:
        company = random.choice(Company.query.all())
        
    name = company.compname 
    comphandle = company.twitter_handle
    tweet_link = construct_tweet_link( comphandle )
    address = company.address
    ktc_score = company.knowthechain_score
    ktc_link = company.knowthechain_link
    website = company.website
    transparency = company.transparency
    watson_query, watson_description = elementary.mydearwatson(name)

    # load labor data into dataframe
    tsv = os.path.join(app.root_path, "../public/world_population.tsv")
    chartdf = pd.read_csv(tsv, sep='\t')
    chartdf = chartdf.loc[:, ["id", "name", "population"]]
    chart_data = chartdf.to_dict(orient='records')

    findat = {}
    goodlist = []

    # query database for country data 
    for g in company.goods:
        goodname = g.goodname
        goodlist.append(goodname)
        countries = [c.countryname for c in g.good_countries]

        # keep only those records that are in the relevant countries
        keepdat = []
        for c in chart_data:
            if c["name"] in countries:
                c["population"] = 75
            else:
                c["population"] = 10
            keepdat.append(c.copy())

        findat[goodname] = keepdat

    chart_data = json.dumps(findat, indent=2)
    data = {'chart_data': chart_data}
 
    table = ibm_query_to_html( watson_query, watson_description)
    return render_template('index.html',
                           comp_name=name,
                           address=address,
                           ktc_score=ktc_score,
                           ktc_link=ktc_link,
                           transparency=transparency,
                           website=website,
                           tweet=tweet_link,
                           data=data,
                           goodlist=goodlist,
                           watson_table=table,
                           watson_description=watson_description)    

@app.route('/test')
def test():
    json_url = os.path.join(app.root_path, "../public/example.json")
    print(json_url)
    dat = json.load(open(json_url))
    return render_template('test.html', data=dat)


@app.route('/data')
def data():
    p = Product.query.get(1)
    return render_template("data.html", product=p.productname)


@app.route('/d3')
def d3():

    comp_name = request.args.get('compname')
    product_name = request.args.get('productname')

    # load population data into dataframe
    tsv = os.path.join(app.root_path, "../public/world_population.tsv")
    df = pd.read_csv(tsv, sep='\t')
    df = df.loc[:, ["id", "name", "population"]]
    chart_data = df.to_dict(orient='records')

    findat = {}
    goodlist = []

    if comp_name is not None:
        comp = db.session.query(Company).filter_by(compname=comp_name).first()
        for g in comp.goods:
            goodname = g.goodname
            goodlist.append(goodname)
            countries = [c.countryname for c in g.good_countries]

            # keep only those records that are in the relevant countries
            keepdat = []
            for c in chart_data:
                if c["name"] in countries:
                    c["population"] = 75
                else:
                    c["population"] = 10
                keepdat.append(c.copy())

            findat[goodname] = keepdat

        chart_data = json.dumps(findat, indent=2)
        data = {'chart_data': chart_data}
        return render_template("d3.html", data=data, goodlist=goodlist)
