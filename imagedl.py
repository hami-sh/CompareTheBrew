"""
script to save images that aren't currently present from the database.

### RUN WITH VPN JUST IN CASE! WE CANNOT BE SURE WHAT BWS BE THINKIN UP HERE ###

"""
from scripts.databaseHandler import *
import os.path
import urllib.request
from random import randint
from time import sleep
import shutil
import requests


def main():
    print("are you sure? you may get banned without vpn [Y/n]")
    s = input()
    if s != 'Y':
        return
    conn = create_connection()
    images = select_image_links(conn)

    i = 0
    print("total: " + str(len(images)))
    for link in images:
        try:
            print(i)
            url = str(link[0])
            url = url.replace("/", "~")
            url = url.replace("?", "+")
            url = url.replace(":", ",")
            url = url.split('~')[-1]
            path = "images/" + url + '.webp'

            if os.path.exists(path):
                print("exists<" + link[0] + ">")
            else:
                print("save<" + link[0] + ">")
                print(path)
                response = requests.get(link[0], stream=True)
                with open(path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
                secs = randint(1, 3)
                sleep(secs)

            i += 1

        except:
            print("-----------------------------------------")
            print("broke")
            print(link)
            print("-----------------------------------------")

    conn = create_connection()
    images = select_image_links(conn)
    conn.close()

    for image in images:
        conn = create_connection()
        print("----")
        save_short_link(conn, image[0])
        conn.close()


if __name__ == "__main__":
    main()
