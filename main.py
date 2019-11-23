#  _____                                    _____ _         ______
# /  __ \                                  |_   _| |        | ___ \
# | /  \/ ___  _ __ ___  _ __   __ _ _ __ ___| | | |__   ___| |_/ /_ __ _____      __
# | |    / _ \| '_ ` _ \| '_ \ / _` | '__/ _ \ | | '_ \ / _ \ ___ \ '__/ _ \ \ /\ / /
# | \__/\ (_) | | | | | | |_) | (_| | | |  __/ | | | | |  __/ |_/ / | |  __/\ V  V /
#  \____/\___/|_| |_| |_| .__/ \__,_|_|  \___\_/ |_| |_|\___\____/|_|  \___| \_/\_/
#                       | |
#                       |_|
#
#
#                          .sssssssss.
#                    .sssssssssssssssssss
#                  sssssssssssssssssssssssss
#                 ssssssssssssssssssssssssssss
#                  @@sssssssssssssssssssssss@ss
#                  |s@@@@sssssssssssssss@@@@s|s
#           _______|sssss@@@@@sssss@@@@@sssss|s
#         /         sssssssss@sssss@sssssssss|s
#        /  .------+.ssssssss@sssss@ssssssss.|
#       /  /       |...sssssss@sss@sssssss...|
#      |  |        |.......sss@sss@ssss......|
#      |  |        |..........s@ss@sss.......|
#      |  |        |...........@ss@..........|
#       \  \       |............ss@..........|
#        \  '------+...........ss@...........|
#         \________ .........................|
#                  |.........................|
#                 /...........................\
#                |.............................|
#                   |.......................|
#                       |...............|
#
#
#           __         __  __ ___      __   __  __  __
#          |_  | |\ | |_  (_   |      |__) |_  |_  |__)
#          |   | | \| |__ __)  |      |__) |__ |__ | \

from classItem import ItemCollection
import argparse
from scrapeBWS import download_bws
from scrapeLiquorLand import download_liquorland

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
    #download_bws(bwsURL, "bws", "txt", total, listBWS)

    # Liquorland
    liquourlandURL = "https://www.liquorland.com.au/search?q=" + args.drink
    listLiquourland = list()
    download_liquorland(liquourlandURL, "liquorland", "txt", total, listLiquourland)

    #


if __name__ == '__main__':
    main()
