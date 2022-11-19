def load_json(jsonfile, portno):
    from pymongo import MongoClient
    import json

    jfile = open(jsonfile, 'r')

    portno = str(portno)
    url = 'mongodb://localhost:' + portno
    client = MongoClient(url)
    db = client["291_db"]
  

    collist = db.list_collection_names()
    if 'dblp' in collist:
        db.drop_collection('dblp')
    
    dblp = db['dblp']


    for line in jfile:
        dblp.insert_one(json.loads(line))

    dblp.create_index([("year", 1)], name="index_year", unique=False)
    dblp.create_index([("id", 1)], name="index_id", unique=True)
    dblp.create_index([("title", 1)], name="index_title", unique=False)
    dblp.create_index([("venue", 1)], name="index_venue", unique=False)
    dblp.create_index([("references", 1)], name="index_ref", unique=False)
    dblp.create_index([("n_citation", 1)], name="index_cit", unique=False)
    dblp.create_index([("abstract", 1)], name="index_abstract", unique=False)
    dblp.create_index([("authors", 1)], name="index_authors", unique=False)


 




