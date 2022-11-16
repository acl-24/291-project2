def add_article(portno):
    from pymongo import MongoClient

    portno = str(portno)
    url = 'mongodb://localhost:' + portno
    client = MongoClient(url)
    db = client["291_db"]
    dblp = db["dblp"]

    while True:
        id = input("Plesae provide the ID of the article: ")
        title = input("Please provide the title of the article: ")
        year = input("Please provide the year the article was published: ")
        authors = input("Please enter the list of authors, separated by comas: ")
        lauthors = authors.split(",")

        ndoc = {}
        testdoc = {}
        ndoc["abstract"] = None
        ndoc["authors"] = lauthors
        ndoc["n_citations"] = 0
        ndoc["references"] = []
        ndoc[" title"] = title
        ndoc["venue"] = None
        ndoc["year"] = year
        ndoc["id"] = id
        testdoc["id"] = id
        
        x = dblp.find_one(testdoc)
        print(x)
        if (x != None):
            print("Article is already in database")
            z = input("Type a to insert another article, or anything else to exit: ")
            if (z == "a"):
                continue
            else:
                break

        else:
            dblp.insert_one(ndoc)
            break

    
    return

add_article(27017)
