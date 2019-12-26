import sqlite3
from sqlite3 import Error
from scripts.classItem import Item
from intellisearch import *
import re
from app import *

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("drinks.db")

        sql = ''' CREATE TABLE IF NOT EXISTS "drinks" ( `ID` INTEGER PRIMARY KEY AUTOINCREMENT, `store` TEXT,
            `brand` BLOB, `name` NUMERIC, `type` TEXT, `price` REAL, `link` TEXT, `ml` REAL, `percent` REAL,
            `stdDrinks` REAL, `efficiency` REAL, `image` TEXT, `shortimage` TEXT )'''
        cur = conn.cursor()
        cur.execute(sql)
        print("connected to database")
    except Error as e:
        print(e)

    return conn

def create_metrics_connection():
    conn = None
    try:
        conn = sqlite3.connect("drinks.db")

        sql = ''' CREATE TABLE IF NOT EXISTS "metrics" ( `ID` INTEGER PRIMARY KEY AUTOINCREMENT, `IP` TEXT,
            `query` TEXT, `datetime` TEXT, `country` TEXT, `region` TEXT, `city` TEXT, `lat` REAL, `long` REAL,
            `hostname` TEXT, `org` TEXT )'''
        cur = conn.cursor()
        cur.execute(sql)
        print("connected to metrics")
    except Error as e:
        print(e)

    return conn

def create_entry(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO drinks(store,brand,name,type,price,link,ml,percent,stdDrinks,efficiency,image)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid

def create_metric_entry(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    print(1)
    sql = ''' INSERT INTO metrics(IP,query,datetime,country,region,city,lat,long,hostname,org)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    print(2)
    cur = conn.cursor()
    print(3)
    cur.execute(sql, task)
    print(4)
    conn.commit()
    ID = cur.lastrowid
    conn.close()
    return ID

def select_all_drinks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM drinks")

    rows = cur.fetchall()

    return rows


def select_all_drinks_by_efficiency(conn):
    """
    Query tasks by efficiency
    :param conn: the Connection object
    :return:
    """
    # Create a new cursor
    cur = conn.cursor()
    # Ececute a new query at the cursor
    cur.execute("SELECT * FROM drinks ORDER BY efficiency DESC")
    # Fetch all of the rows that matched the query
    rows = cur.fetchall()
    return rows


def select_all_drinks_by_worst_efficiency(conn):
    """
    Query tasks by efficiency
    :param conn: the Connection object
    :return:
    """
    # Create a new cursor
    cur = conn.cursor()
    # Ececute a new query at the cursor
    cur.execute("SELECT * FROM drinks ORDER BY efficiency ASC")
    # Fetch all of the rows that matched the query
    rows = cur.fetchall()
    return rows


def select_all_drinks_by_cost_asc(conn):
    """
    Query tasks by price ascending
    :param conn: the Connection object
    :return:
    """
    # Create a new cursor
    cur = conn.cursor()
    # Ececute a new query at the cursor
    cur.execute("SELECT * FROM drinks ORDER BY price ASC")
    # Fetch all of the rows that matched the query
    rows = cur.fetchall()

    return rows


def select_all_drinks_by_cost_desc(conn):
    """
    Query tasks by price descending
    :param conn: the Connection object
    :return:
    """
    # Create a new cursor
    cur = conn.cursor()
    # Ececute a new query at the cursor
    cur.execute("SELECT * FROM drinks ORDER BY price DESC")
    # Fetch all of the rows that matched the query
    rows = cur.fetchall()

    return rows


def select_all_drinks_between_cost(conn, value1, value2):
    """
    Query tasks by selecting drinks between a cost
    :param conn: the Connection object
    :return:
    """
    # Create a new cursor
    cur = conn.cursor()

    # Ececute a new query at the cursor
    cur.execute("SELECT * FROM drinks WHERE price BETWEEN {} AND {} ORDER BY efficiency DESC".format(value1, value2))
    # Fetch all of the rows that matched the query
    rows = cur.fetchall()

    return rows


def select_drink_by_efficiency_and_type(conn, type):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param type: the value in the type column that we are querying for
    :param priority:
    :return:
    """
    # Create a new cursor
    cur = conn.cursor()
    # Execute a new query at the cursor
    cur.execute("SELECT * FROM drinks WHERE type LIKE '%{}%' ORDER BY efficiency DESC".format(type))
    # Fetch all of the rows that matched the query
    rows = cur.fetchall()

    return rows


def select_image_links(conn):
    """
    Query all image links
    :param conn: the Connection object
    :return:
    """
    # Create a new cursor
    cur = conn.cursor()
    # Execute a new query at the cursor
    cur.execute("SELECT image FROM drinks")
    # Fetch all of the rows that matched the query
    rows = cur.fetchall()

    return rows

# def functionRegex(value, pattern):
#     print(r"/^" + pattern.lower() + r"| {1}" + pattern.lower() + r"/gm")
#     c_pattern = re.compile(r"\^" + pattern.lower() + r"| {1}" + pattern.lower() + r"/gm")
#     return c_pattern.search(value) is not None


def select_drink_by_smart_search(conn, terms):
    """Select all drinks that contain any of the search keywords given in their name, brand or type attributes
    
    Args:
        param1: the Connection object
        param2: the value in the type/name/brand column that we are querying for

    Returns:
        A list of rows from the drinks table matching the search terms
    """
    # conn.create_function('regexp', 2, functionRegex)
    # Create a new cursor
    cur = conn.cursor()
    # Define a new list for which to store our final list of results
    results = list()

    # Split the search keyboards by the spaces in between words
    inputs = terms.split(" ")
    print("SEARCH TERMS: " + str(inputs))
    # return termsList
    terms = list()
    for term in inputs:
        terms.append(term.lower())
    print("-------------------<OLD>-------------------")
    print(terms)
    # now run intellisense search to get better result parity
    print("-------------------(NEW)-------------------")
    intelliterms = intellisearch(terms)
    # print(intelliterms)

    # For each keyword, execute a new query at the cursor to find drinks matching that keyword
    for term in intelliterms:
        # cur.execute("SELECT * FROM drinks WHERE type LIKE '%{}
        term = term.lower()
        cur.execute(
            "SELECT * FROM drinks WHERE type LIKE '%{}%' OR name LIKE '%{}%' OR brand LIKE '%{}%' ORDER BY efficiency DESC".format(
                term, term, term))
        # cur.execute('SELECT * FROM drinks WHERE REGEXP(type, ?) OR REGEXP(name, ?) OR REGEXP(brand, ?) ORDER BY efficiency DESC', (term, term, term,))

        rows = cur.fetchall()
        print("FOR " + term)

        print("NUMBER OF ROWS FOUND: " + str(len(rows)))
        # For each row in rows, if the row is not already in the results list add it
        for row in rows:
            if not (row in results):
                # print(row[2], row[3], row[4])
                # print(re.match(r"^"+term+"| {1}"+term, row[2].lower(), re.M))
                # print(re.match(r"^"+term+"| {1}"+term, row[3], re.M))
                # print(re.match(r"^"+term+"| {1}"+term, row[4], re.M))
                if re.search(r'^'+term+'| {1}'+term, row[2].lower(), re.M) or re.search(r'^'+term+'| {1}'+term, row[3].lower(), re.M)\
                        or re.search(r'^'+term+'| {1}'+term, row[4].lower(), re.M):
                    # print("HERE")
                    # print(row)
                    results.append(row)

    print("NUMBER OF RESULTS FOUND: " + str(len(results)))
    # organise results based on efficiency - currently only sorted per term.
    results.sort(key=lambda tup: tup[10], reverse=True)

    # Return the final list of results
    return results


def update_drink(conn, drink, newPrice):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param drink:
    :return: project id
    """
    sql = ''' UPDATE drinks
              SET price = ?, link = ?, image = ?, efficiency = ?
              WHERE name = ?
              AND brand = ?
              AND store = ? '''

    result = get_drinks_stddrinks(conn, drink)
    if result == False:
        print("failed to update drink... here are the details")
        try:
            print(drink)
        except:
            print("couldnt print drink!")
    else:
        print('---------------')
        print(drink.brand + " " + drink.name)
        cur = conn.cursor()
        cur.execute(sql, (
        newPrice, drink.link, drink.image, float(float(result) / float(newPrice)), drink.name, drink.brand,
        drink.store))
        print(float(newPrice))
        print(float(result))
        print(float(result)/float(newPrice))
        conn.commit()


def is_drink_in_table(conn, drink):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param drink:
    :return: project id
    """
    sql = ''' SELECT * FROM drinks
              WHERE store = ?
              AND brand = ?
              AND name = ?
              AND link = ?
              '''
    cur = conn.cursor()
    cur.execute(sql, (drink.store, drink.brand, drink.name, drink.link))

    rows = cur.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False


def get_drinks_stddrinks(conn, drink):
    """
    get the standard drinks of a drink
    :param conn:
    :param drink:
    :return: project id
    """
    sql = ''' SELECT * FROM drinks
              WHERE store = ?
              AND brand = ?
              AND name = ?
              '''
    cur = conn.cursor()
    cur.execute(sql, (drink.store, drink.brand, drink.name))

    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][9]
    else:
        return False


def save_short_link(conn, image):
    """
    get the standard drinks of a drink
    :param conn:
    :param drink:
    :return: project id
    """
    sql = ''' UPDATE drinks
              SET shortimage = ?
              WHERE image = ? '''
    cur = conn.cursor()

    if image != None:
        url = str(image)
        oldurl = url
        url = url.replace("/", "~")
        url = url.replace("?", "+")
        url = url.replace(":", ",")
        print(url)
        url = url.split('~')[-1]
        shortimage = url.split("'")[0]
        print(shortimage)
        print(oldurl)
        cur.execute(sql, (shortimage, oldurl))
        conn.commit()
        print('done')


def fix_missing_beer_images(conn):
    """
    get the standard drinks of a drink
    :param conn:
    :param drink:
    :return: project id
    """
    drinks = select_all_drinks(conn)
    emptyImageDrinks = list()

    for drink in drinks:
        print(drink[11])
        if drink[11] is None:
            emptyImageDrinks.append(drink)

    print(len(emptyImageDrinks))

    for empty in emptyImageDrinks:
        for drink in drinks:
            old_empty = empty[3].split("-")[0]
            old_drink = drink[3].split("-")[0]
            if old_empty == old_drink:
                if empty[0] != drink[0]:
                    if empty[2] == drink[2]:
                        if empty[11] is None:
                            if drink[11] is not None:
                                print("--------------------------------")
                                print(drink)
                                print(empty)
                                sql = ''' UPDATE drinks
                                          SET shortimage = ?, image = ?
                                          WHERE name = ? '''
                                cur = conn.cursor()
                                cur.execute(sql, (drink[12], drink[11], empty[3]))
                                conn.commit()


def dbhandler(conn, list, mode):
    # populate or update mode
    if mode == "p":
        for drink in list:
            drink_task = (
            drink.store, drink.brand, drink.name, drink.type, float(drink.price), drink.link, float(drink.ml),
            float(drink.percent), float(drink.stdDrinks), float(drink.efficiency), drink.link)
            create_entry(conn, drink_task)

    elif mode == "u":
        # update entries with the same name / add entries who's names do not exist.
        for drink in list:
            if is_drink_in_table(conn, drink):
                print('//update')
                update_drink(conn, drink, drink.price)

            else:
                print('//create')
                drink_task = (drink.store, drink.brand, drink.name, drink.type, float(drink.price), drink.link,
                              float(drink.ml), float(drink.percent), float(drink.stdDrinks), float(drink.efficiency),
                              drink.image)
                create_entry(conn, drink_task)

    conn.commit()


def delete_task(conn, name, brand, store, type):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM tasks WHERE name=? AND brand=? AND store=? AND type=?'
    cur = conn.cursor()
    cur.execute(sql, (name, brand, store, type))
    conn.commit()


def delete_all(conn):
    """
        Delete a task by task id
        :param conn:  Connection to the SQLite database
        :param id: id of the task
        :return:
        """
    sql = 'DELETE FROM drinks'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
