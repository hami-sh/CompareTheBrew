from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
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
    return render_template('index.html')

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
    # Get results the old way - by running the whole scrape script for every request
    # tempResults = search(searchTerms)

    # Get results the new way - by querying the database
    conn = db.create_connection() # connect to the database

    # This is the wortking query of all drinks
    # tempResults = db.select_all_drinks_by_efficiency(conn) # get all drinks where the value in column 'type' is 'searchTerms' sorted by efficiency
    # This is the broken query by type
    tempResults = db.select_drink_by_efficiency_and_type(conn, searchTerms) # get all drinks where the value in column 'type' is 'searchTerms' sorted by efficiency

    # Print a summary of the search results sent to the client on the server command prompt (should also be logged in future)
    print("")
    print("")
    print("                                    SEARCH RESULTS                                     ")
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    # print("Now that the database is hooked up there are too many results to show. Sorry for any inconvenience.")
    # for result in tempResults:
    #     print("TYPE: " + str(result[3]))
    print(tempResults)
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("")
    print("")
    return render_template('results.html', results=tempResults)


# # Basic test page for url /hello
# @app.route('/test1')
# def hello():
#     return "Hello World!"

# # A second test page now rendering a basic html page
# @app.route('/<string:page_name>/')
# def render_static(page_name):
#     return render_template('%s.html' % page_name)

# # A function to get search results from a page
# @app.route('/results', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     print("OLD: " + text)
#     # processed_text = text.upper()
#     return text

# @app.route('/<string:page_name>/')
# def render_static(page_name):
#     return render_template('%s.html' % page_name)


# Run the flask application (won't run when the site is being hosted on a server)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
