from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
from datetime import datetime
import re
import json
from urllib.request import urlopen

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
    conn = db.create_connection() # connect to the database
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
    return redirect("/results/" + searchTerms)

# A third test page to display search results
@app.route("/results/<searchTerms>")
def displayResultPage(searchTerms):
    """
    Displays the search results page given the search terms

    Args:
        searchTerms: the searchTerms entered in the search (currently just the initial search terms entered)
    Returns:
        the rendered html template for the page
    """
    # Get results the new way - by querying the database
    conn = db.create_connection() # connect to the database
    tempResults = db.select_drink_by_smart_search(conn, searchTerms) # get drinks with type/brand/name matching any of the words in searchTerms

    # # This is the working query of all drinks
    # # tempResults = db.select_all_drinks_by_efficiency(conn) # get all drinks where the value in column 'type' is 'searchTerms' sorted by efficiency
    # # This is the broken query by type
    # # tempResults = db.select_drink_by_efficiency_and_type(conn, searchTerms) # get all drinks where the value in column 'type' is 'searchTerms' sorted by efficiency

    # Print a summary of the search results sent to the client on the server command prompt (should also be logged in future)
    # print("""\n\n                                    SEARCH RESULTS                                     \n|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||""")
    # for result in tempResults:
    #     print(result)
    # print("""|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n\n""")


    # gather metrics info
    TOQ = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
    print(TOQ)
    query = ""
    for term in searchTerms:
        query += term
    print(query)
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    hostname = data['hostname']
    print(hostname)
    IP = data['ip']
    print(IP)
    org = data['org']
    print(org)
    city = data['city']
    print(city)
    country = data['country']
    print(country)
    region = data['region']
    location = data['loc']
    lat = location.split(",")[0]
    long = location.split(",")[1]

    print(region)
    print(lat)
    print(long)

    metconn = db.create_metrics_connection()
    metric = (str(IP), str(query), str(TOQ), str(country), str(region), str(city), float(lat), float(long), str(hostname), str(org))
    ID = db.create_metric_entry(metconn, metric)
    print("ID: " + str(ID))
    return render_template('results.html', results=tempResults)

# # A function to get search terms from the search bar on the results page
@app.route('/results/<arg>', methods=['POST'])
def postNewSearchTerms(arg):
    """
    ...
    """
    # Get the search terms inputted by the user
    searchTerms = request.form['searchTerms']
    print("SEARCH TERMS ENTERED BY USER: " + searchTerms)

    # Send the user to the results page
    return redirect("/results/" + searchTerms)

# Route for About Us page
@app.route('/about', methods=['GET', 'POST'])
def viewabout():
    return render_template('About.html')  # render a template

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

# Hamish Section
@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


# Run the flask application (won't run when the site is being hosted on a server)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    #app.run(host='127.0.0.1', port=8000, debug=True)
