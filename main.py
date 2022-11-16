#main.py does importing json file and creating a mainScreen 

import sys
import pymongo
import mainScreen as ms
import time

lj = __import__('load-json')

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please enter a valid database file!!")
    else:
        if len(sys.argv) > 2:
            print("Error usage! Usage:main.py [json_name.json]")
        else:
            if sys.argv[1].endswith(".json"):
                    port = int(input('please input a port number: '))
                    db, dblp = lj.load_json(sys.argv[1], port)
                    time.sleep(1)
                    ms.mainScreen(db, dblp)
            else:
                print("The input file name is not a file name ending in '. json'")
