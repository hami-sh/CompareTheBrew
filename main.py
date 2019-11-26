#  _____                                    _____ _         ______
# /  __ \                                  |_   _| |        | ___ \
# | /  \/ ___  _ __ ___  _ __   __ _ _ __ ___| | | |__   ___| |_/ /_ __ _____      __
# | |    / _ \| '_ ` _ \| '_ \ / _` | '__/ _ \ | | '_ \ / _ \ ___ \ '__/ _ \ \ /\ / /
# | \__/\ (_) | | | | | | |_) | (_| | | |  __/ | | | | |  __/ |_/ / | |  __/\ V  V /
#  \____/\___/|_| |_| |_| .__/ \__,_|_|  \___\_/ |_| |_|\___\____/|_|  \___| \_/\_/
#                       | |
#                       |_|
from classItem import ItemCollection
from scrape import getData
import argparse
import threading

# logging.basicConfig(filename='brew.log', filemode='w', format='[%(asctime)s]%(name)s:%(levelname)s:%(message)s')
# console = logging.StreamHandler()
# console.setLevel(print)
# # set a format which is simpler for console use
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# # tell the handler to use this format
# console.setFormatter(formatter)
# # add the handler to the root logger
# logging.getLogger('').addHandler(console)

def main():
    parser = argparse.ArgumentParser(description='Enter alcohol to search')
    parser.add_argument("--drink", default='vodka', help="The drink")
    args = parser.parse_args()
    controller(args)


def controller(args):
    """
    Main controller of URL execution
    """
    # Total collection of items
    # Scrape from the given search url with the given search term
    bwsData = list()
    # url = "https://bws.com.au/search?searchTerm=" + args.drink
    url = "https://bws.com.au/search?searchTerm=balter"# + args.drink
    # url = "https://www.firstchoiceliquor.com.au/search?searchTerm=" + args.drink
    bwsData = scrape(url)

    # Liquorland
    # liquourlandURL = "https://www.liquorland.com.au/search?q=" + args.drink
    # listLiquourland = list()
    # download_liquorland(liquourlandURL, "liquorland", "txt", total, listLiquourland)


if __name__ == '__main__':
    main()
