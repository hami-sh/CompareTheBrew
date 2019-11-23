##############################################
##############################################
# Hamish Bultitude 2019
##############################################
##############################################

from classItem import ItemCollection
import argparse
from scrapeBWS import download_bws

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
    total = ItemCollection()
    # BWS
    bwsURL = "https://bws.com.au/search?searchTerm=" + args.drink
    listBWS = list()
    download_bws(bwsURL, "bws", "txt", total, listBWS)

    # Liquorland

    #


if __name__ == '__main__':
    main()
