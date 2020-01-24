from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import current_app
from flask import jsonify
from datetime import datetime
import re
import json
from urllib.request import urlopen
import ipinfo
import random

# from scrape2 import search
import scripts.databaseHandler as db

# Create a new flask application
app = Flask(__name__)

# Working serve of the search page with css and js
@app.route("/")
def displaySearchPage():
    """
    ...
    """
    # Get the current top drink from the database
    conn = db.create_connection()  # connect to the database
    topDrink = db.select_all_drinks_by_efficiency(conn)[0] # get the first result from all of the drinks sorted by efficiency desc
    return render_template('index.html', result=topDrink)

# A function to get search terms from the search page
@app.route('/', methods=['POST'])
def postSearchTerms():
    """
    ...
    """
    # Get the search terms inputted by the user
    searchTerms = request.form['searchTerms']
    print("SEARCH TERMS ENTERED BY USER: " + searchTerms)

    # Send the user to the results page
    return redirect("/results=score-desc/" + searchTerms)

# --------------------------------------
#
#                 SCORE (best)
#
# --------------------------------------
@app.route("/results=score-desc/<searchTerms>")
def display_bestscore_ResultPage(searchTerms):
    """
    Displays the search results page given the search terms

    Args:
        searchTerms: the searchTerms entered in the search (currently just the initial search terms entered)
    Returns:
        the rendered html template for the page
    """
    # Get results the new way - by querying the database
    conn = db.create_connection() # connect to the database
    tempResults = db.select_drink_by_smart_search(conn, searchTerms, 'DESC_efficiency')
    # insert_ads_amongst_results(tempResults)

    # gather metrics info
    metrics(searchTerms)
    return render_template('results.html', results=tempResults)


# --------------------------------------
#
#                 SCORE (worst)
#
# --------------------------------------
@app.route("/results=score-asc/<searchTerms>")
def display_worstscore_ResultPage(searchTerms):
    """
    Displays the search results page given the search terms

    Args:
        searchTerms: the searchTerms entered in the search (currently just the initial search terms entered)
    Returns:
        the rendered html template for the page
    """
    # Get results the new way - by querying the database
    conn = db.create_connection()  # connect to the database
    tempResults = db.select_drink_by_smart_search(conn, searchTerms, 'ASC_efficiency')
    # insert_ads_amongst_results(tempResults)

    # gather metrics info
    metrics(searchTerms)
    return render_template('results.html', results=tempResults)


# --------------------------------------
#
#                 PRICE (asc)
#
# --------------------------------------
@app.route("/results=price-asc/<searchTerms>")
def display_bestprice_ResultPage(searchTerms):
    """
    Displays the search results page given the search terms

    Args:
        searchTerms: the searchTerms entered in the search (currently just the initial search terms entered)
    Returns:
        the rendered html template for the page
    """
    # Get results the new way - by querying the database
    conn = db.create_connection()  # connect to the database
    tempResults = db.select_drink_by_smart_search(conn, searchTerms, 'ASC_price')
    # insert_ads_amongst_results(tempResults)

    # gather metrics info
    metrics(searchTerms)

    return render_template('results.html', results=tempResults)

# --------------------------------------
#
#                 PRICE (desc)
#
# --------------------------------------
@app.route("/results=price-desc/<searchTerms>")
def display_worstprice_ResultPage(searchTerms):
    """
    Displays the search results page given the search terms

    Args:
        searchTerms: the searchTerms entered in the search (currently just the initial search terms entered)
    Returns:
        the rendered html template for the page
    """
    # Get results the new way - by querying the database
    conn = db.create_connection()  # connect to the database
    tempResults = db.select_drink_by_smart_search(conn, searchTerms, 'DESC_price')
    # insert_ads_amongst_results(tempResults)

    # gather metrics info
    metrics(searchTerms)

    return render_template('results.html', results=tempResults)

# --------------------------------------
#
#                 size of drink (desc)
#
# --------------------------------------
@app.route("/results=size-desc/<searchTerms>")
def display_largest_ResultPage(searchTerms):
    """
    Displays the search results page given the search terms

    Args:
        searchTerms: the searchTerms entered in the search (currently just the initial search terms entered)
    Returns:
        the rendered html template for the page
    """
    # Get results the new way - by querying the database
    conn = db.create_connection()  # connect to the database
    tempResults = db.select_drink_by_smart_search(conn, searchTerms, 'DESC_ml')
    # insert_ads_amongst_results(tempResults)

    # gather metrics info
    metrics(searchTerms)

    return render_template('results.html', results=tempResults)

# --------------------------------------
#
#                 size of drink (asc)
#
# --------------------------------------
@app.route("/results=size-asc/<searchTerms>")
def display_smallest_ResultPage(searchTerms):
    """
    Displays the search results page given the search terms

    Args:
        searchTerms: the searchTerms entered in the search (currently just the initial search terms entered)
    Returns:
        the rendered html template for the page
    """
    # Get results the new way - by querying the database
    conn = db.create_connection()  # connect to the database
    tempResults = db.select_drink_by_smart_search(conn, searchTerms, 'ASC_ml')
    # insert_ads_amongst_results(tempResults)

    # gather metrics info
    metrics(searchTerms)

    return render_template('results.html', results=tempResults)

# --------------------------------------
#
#                 pecent (desc)
#
# --------------------------------------
@app.route("/results=percent-desc/<searchTerms>")
def display_largepercent_ResultPage(searchTerms):
    """
    Displays the search results page given the search terms

    Args:
        searchTerms: the searchTerms entered in the search (currently just the initial search terms entered)
    Returns:
        the rendered html template for the page
    """
    # Get results the new way - by querying the database
    conn = db.create_connection()  # connect to the database
    tempResults = db.select_drink_by_smart_search(conn, searchTerms, 'DESC_percent')
    # insert_ads_amongst_results(tempResults)

    # gather metrics info
    metrics(searchTerms)

    return render_template('results.html', results=tempResults)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                 advert insert
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def insert_ads_amongst_results(tempResults):
    num_ads = 0  # hom wnay ads are currently added to the list
    next_ad_index = 1  # the index we will place the next ad item at
    drinks_per_ad = 5  # hom many legitimate drinks cards (-1) we will have until we show the next drink card  i.e. 3 = 1 ad per 3 drinks
    while next_ad_index < len(tempResults):  # While we have not yet finished putting ads all through the list
        tempResults.insert(next_ad_index, ['GOOGLE_AD'])  # Add an advertisement item to the list
        num_ads = num_ads + 1  # increment the number of ads we have added to the page
        next_ad_index = (num_ads * drinks_per_ad) + random.randint(1,
                                                                   drinks_per_ad)  # calculate the position in which we will put the next drink card
    return tempResults


def metrics(searchTerms):
    try:
        TOQ = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
        print(TOQ)
        query = ""
        for term in searchTerms:
            query += term
        print(query)
        access_token = 'a7a5ae20cc1be2'
        handler = ipinfo.getHandler(access_token)
        IP = ""
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            IP = request.environ['REMOTE_ADDR']
        else:
            IP = request.environ['HTTP_X_FORWARDED_FOR']  # if behind a proxy
        print(IP)
        details = handler.getDetails(IP)
        print(details.all)
        hostname = ""
        print(hostname)
        org = ""
        print(org)
        city = ""
        print(city)
        country = details.country_name
        print(country)
        region = ""
        lat = details.latitude
        long = details.longitude

        print(region)
        print(lat)
        print(long)

        metconn = db.create_metrics_connection()
        metric = (
            str(IP), str(query), str(TOQ), str(country), str(region), str(city), float(lat), float(long), str(hostname),
            str(org))
        ID = db.create_metric_entry(metconn, metric)
        print("ID: " + str(ID))
    except Exception as e:
        print(e)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#            top50page
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route("/top50/beer")
def display_top50_page():
    # Get results the new way - by querying the database
    conn = db.create_connection()  # connect to the database
    tempResults = db.select_drink_by_smart_search(conn, "beer", 'DESC_efficiency')
    # insert_ads_amongst_results(tempResults)

    # gather metrics info
    metrics(["beer"])
    return render_template('top50.html', results=tempResults)

@app.route("/top50/wine")
def display_top50wine_page():
    # Get results the new way - by querying the database
    conn = db.create_connection()  # connect to the database
    tempResults = db.select_drink_by_smart_search(conn, "wine", 'DESC_efficiency')
    # insert_ads_amongst_results(tempResults)

    # gather metrics info
    metrics(["wine"])
    return render_template('top50.html', results=tempResults)

@app.route("/top50/spirits")
def display_top50spirits_page():
    # Get results the new way - by querying the database
    conn = db.create_connection()  # connect to the database
    tempResults = db.select_drink_by_smart_search(conn, "spirits", 'DESC_efficiency')
    # insert_ads_amongst_results(tempResults)

    # gather metrics info
    metrics(["spirits"])
    return render_template('top50.html', results=tempResults)

# # A function to get search terms from the search bar on the results page
@app.route('/results=score-desc/<arg>', methods=['POST'])
@app.route('/results=score-asc/<arg>', methods=['POST'])
@app.route('/results=price-desc/<arg>', methods=['POST'])
@app.route('/results=size-desc/<arg>', methods=['POST'])
@app.route("/top50/beer")
@app.route("/top50/wine")
@app.route("/top50/spirits")

def postNewSearchTerms(arg):
    """
    ...
    """
    print("LOG: INSIDE")
    # Get the search terms inputted by the user
    searchTerms = request.form['searchTerms']
    print("SEARCH TERMS ENTERED BY USER: " + searchTerms)

    # Send the user to the results page
    return redirect("/results=score-desc/" + searchTerms)

# Route for About Us page
# @app.route('/about', methods=['GET', 'POST'])
# def viewabout():
#     return render_template('About.html')  # render a template

# Route for About Us page
@app.route('/faq', methods=['GET', 'POST'])
def viewFAQ():
    return render_template('FAQ.html')  # render a template

# Ajunner Error Handling
# 404
@app.errorhandler(404)
def page_not_found404(e):
    return render_template('/404.html'), 404

# 500
@app.errorhandler(500)
def page_not_found500(e):
    return render_template('/500.html'), 500

@app.route('/api', methods=['GET', 'POST'])
def api_handler():
    term = request.args.get('term')
    order = request.args.get('order')
    print(term)
    print(order)

    # Get results the new way - by querying the database
    conn = db.create_connection()  # connect to the database
    tempResults = []
    # gather metrics info
    metrics(term)

    if order == "score_desc":
        tempResults = db.select_drink_by_smart_search(conn, term, 'DESC_efficiency')
    elif order == "score_asc":
        tempResults = db.select_drink_by_smart_search(conn, term, 'ASC_efficiency')
    elif order == "price_desc":
        tempResults = db.select_drink_by_smart_search(conn, term, 'DESC_price')
    elif order == "size_desc":
        tempResults = db.select_drink_by_smart_search(conn, term, 'DESC_ml')

    print(tempResults)

    data = {}

    # loop over tuples
    i = 0
    for result in tempResults:
        drink = dict()
        drink['id'] = result[0]
        drink['store'] = result[1]
        drink['brand'] = result[2]
        drink['name'] = result[3]
        drink['type'] = result[4]
        drink['price'] = result[5]
        drink['url'] = result[6]
        drink['volume'] = result[7]
        drink['percent'] = result[8]
        drink['drinks'] = result[9]
        drink['efficiency'] = result[10]
        drink['imglink'] = result[11]
        drink['img'] = result[12]
        data[i] = drink
        i = i + 1

    # return json_data
    return current_app.response_class(json.dumps(data), mimetype="application/json")
    # return jsonify({'ip': request.remote_addr}), 200


# Run the flask application (won't run when the site is being hosted on a server)
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=True)
    app.run(host='127.0.0.1', port=8000, debug=True)
