def load_json(jsonfile, portno):
    from pymongo import MongoClient
    import json

    jfile = open(jsonfile, 'r')

    newdocs = []
    for line in jfile:
        newdocs.append(json.loads(line))
    portno = str(portno)
    url = 'mongodb://localhost:' + portno
    client = MongoClient(url)
    db = client["291_db"]

    collist = db.list_collection_names()
    if 'dblp' in collist:
        db.drop_collection('dblp')
    
    dblp = db['dblp']

    dblp.insert_many(newdocs)

    return

#tests
load_json('dblp-ref-10.json', 27017)




