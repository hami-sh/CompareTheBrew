import os.path
from os import path
import csv
import datetime

def sqlhandler(list, mode):
    # if path.exists('drinks.csv') == False:
        # with open('drinks.csv', newline='') as drinks:
            # drinks.write("#INFO#," + str(datetime.datetime) + "," + str(len(list)))

    # append or update mode
    if mode == "append":
        with open('drinks.csv', mode='w') as employee_file:
            writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['INFO', str(datetime.datetime.today()), len(list)])

            for drink in list:
                writer.writerow(drink.brand + " " + drink.name, drink.stddrinks, drink.price, drink.link)


    #
    # elif mode == "update":
    #     update entries with the same name / add entries who's names do not exist.
        # print(1)




