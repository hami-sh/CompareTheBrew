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
    #s = input()
    #if s != 'Y':
    #    return
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
            uncompressed_path = "static/images/uncompressed/" + url + '.webp'
            compressed_path = "static/images/drinkimages/" + url + '.png'
            if os.path.exists(compressed_path):
                print("exists<" + link[0] + ">")
            else:
                print("save<" + link[0] + ">")
                print(uncompressed_path)
                response = requests.get(link[0], stream=True)
                with open(uncompressed_path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
                secs = randint(1, 3)
                print("sleeping " + str(secs) + ". . .")
                sleep(secs)

            i += 1

        except Exception as e:
            print("-----------------------------------------")
            print("broke")
            print(link)
            print(e)
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
