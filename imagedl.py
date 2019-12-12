"""
script to save images that aren't currently present from the database.

### RUN WITH VPN JUST IN CASE! WE CANNOT BE SURE WHAT BWS BE THINKIN UP HERE ###

"""
from scripts.databaseHandler import *
import os.path
import urllib.request
from random import randint
from time import sleep

def main():
    print(1)
    conn = create_connection()
    images = select_image_links(conn)

    i = 0
    print("total: " + str(len(images)))
    for link in images:
        print(i)
        print(link[0])
        # if os.path.exists("images/" + link[0]):
        #     print("exists<" + link[0] + ">")
        # else:
        #     print("save<" + link[0] + ">")
        #     urllib.request.urlretrieve(link[0], str("images/" + link[0]))
        # i += 1
        #
        # if i == 1:
        #     break
        # secs = randint(1, 3)
        # sleep(secs)


def davo():
    print(1)
    conn = create_connection()
    images = select_all_drinks(conn)

    i = 0
    print("total: " + str(len(images)))
    for link in images:
        print(link[0])
        # if os.path.exists("images/" + link[0]):
        #     print("exists<" + link[0] + ">")
        # else:
        #     print("save<" + link[0] + ">")
        #     urllib.request.urlretrieve(link[0], str("images/" + link[0]))
        # i += 1
        #
        # if i == 1:
        #     break
        # secs = randint(1, 3)
        # sleep(secs)

if __name__ == "__main__":
    # main()
    davo()