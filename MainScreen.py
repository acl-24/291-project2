import sys
import pymongo
import uuid
from pymongo.collation import Collation
import re

def error_msg(str):
    error_str_line = "\n************************\n"
    print(error_str_line + str + error_str_line)

def info_msg(str):
    info_str_line = "\n-------------------------\n"
    print(info_str_line + str + info_str_line)


class mainScreen():
    def __init__(self, db, dblp):
        self.db = db
        self.collection = dblp
        self.article_search_result = []
        self.article_page = 0

        self.main_screen(db, dblp)
        
    def main_screen(self, db, dblp):
        self.db = db
        self.dblp = dblp
        while True:
            print('''
                        ==============Artist Screen=================
                        |   [1.Search for Articles              ]  |
                        |   [2.Search for Authors               ]  |
                        |   [3.List the Venues                  ]  |
                        |   [4.Add an Article                   ]  |
                        ============================================
                        ''')
            #basic input handling
            try:
                option = int(input('Please enter the option you want to choose(1/2/3/4):'))
            except ValueError:
                error_msg("Error: Invalid input")
                option = int(input('Please enter the option you want to choose(1/2/3/4):'))
            
            if option == 1:
                # The user should be able to provide one or more keywords, and the system should retrieve all articles 
                # that match all those keywords (AND semantics). A keyword matches if it appears in any of title, authors, abstract, 
                # venue and year fields (the matches should be case-insensitive). For each matching article, display the id, 
                # the title, the year and the venue fields. The user should be able to select an article to see all fields including 
                # the abstract and the authors in addition to the fields shown before. If the article is referenced by other articles, 
                # the id, the title, and the year of those references should be also listed.

                print("=====Search for articles=====")
                text = input("Search text:")
                if len(text) == 0:
                    return
                query_word_list = ["title", "authors", "abstract", "venue"]
                presentable = []

                for query_word in query_word_list:
                    query_segment = {query_word : text}
                    result_list = dblp.find(
                        query_segment, 
                        {"_id" : 0, "id" : 1, "title" : 1, "year" : 1, "venue" : 1}).collation(Collation(locale= 'en', strength= 2))
                    exist_flag = False
                    for i in result_list:
                        for j in presentable:
                            if i["id"] == j["id"]:
                                exist_flag = True
                        
                        if (exist_flag == False):
                            presentable.append(i)
                        exist_flag = False
                        
                
                try:
                    keyword_year = int(text)
                    result_year_list = dblp.find(
                        {"year" : keyword_year}, 
                        {"_id" : 0, "id" : 1, "title" : 1, "year" : 1, "venue" : 1})
                    exist_flag = False
                    for i in result_year_list:
                        for j in presentable:
                            if i["id"] == j["id"]:
                                exist_flag = True
                        
                        if (exist_flag == False):
                            presentable.append(i)
                        exist_flag = False
                except Exception:
                    pass
       
                print("==========Search Result==========")
                for x in presentable:
                    print(x)

                self.select_article(db, dblp, presentable)


            elif option == 2:
                # The user should be able to provide a keyword  and see all authors whose names contain the keyword 
                # (the matches should be case-insensitive). For each author, list the author name and the number of publications.
                #  The user should be able to select an author and see the title, year and venue of all articles by that author. 
                #  The result should be sorted based on year with more recent articles shown first.
                print("=====Search for authors=====")
                text = input("Search text:")
                if len(text) == 0:
                    return
                author_result = dblp.find(
                    {"$text": {"$search": text}},
                    {"_id" : 0, "authors" : 1}
                    )

                author_list = []
                for x in author_result:
                    for y in x['authors']:
                        if re.search(text, y, re.IGNORECASE):
                            if y not in author_list:
                                author_list.append(y)


                print("==========Search Result==========")
                presentable = []
                for i in author_list:
                    result = dblp.aggregate(
                        [
                            {"$match" : {"authors" : i}},
                            {"$unwind" : "$authors"},
                            {"$match" : {"authors" : i}},
                            {"$group": {"_id" : "$authors", "n_wrote" : {"$sum" : 1}}}
                        ]
                    )

                    for x in result:
                        presentable.append(x)

                for x in presentable:
                        print(x)
                
                self.select_author(db, dblp, presentable)

            # elif option == 3:
            #     # The user should be able to enter a number n and see a listing of top n venues. For each venue, list the venue, 
            #     # the number of articles in that venue, and the number of articles that reference a paper in that venue. 
            #     # Sort the result based on the number of papers that reference the venue with the top most cited venues shown first. 
            
            elif option == 4:
            #     # The user should be able to add an article to the collection by providing a unique id, a title, a list of authors, 
            #     # and a year. The fields abstract and venue should be set to null, references should be set to an empty array and 
            #     # n_citations should be set to zero. 
                print("=====Add Article: =====")
                self.add_article()
            
            elif option == 5:
                return
            
            else:
                error_msg("Error: Invalid input")

    def select_article(self, db, dblp, presentable):
        while True:
            print("==========Search Result==========")
            print('''
                ==============options=============
                |   [1.Select               ]    |
                |   [2.Back                 ]    |
                ==================================
                ''')

            option = int(input("Enter the choice you would like to select: "))
            if option == 1:
                select = int(input("Enter the index of the item you want to choose: "))
                if select>len(presentable) or select<=0:
                    error_msg("Error: Invalid input")
                else:
                    print("=========Get more information=========")
                    selected_id = presentable[select - 1]["id"]
                    select_result = dblp.find(
                        {"id" : {"$eq" : selected_id}}, 
                        {"_id" : 0, "id" : 1, "title" : 1, "year" : 1, "venue" : 1, "authors" : 1, "abstract" : 1})
                    for x in select_result:
                        print(x)
                    print("=========Other References=========")
                    reference_result = dblp.find(
                        {"references" : selected_id},
                        {"_id" : 0, "id" : 1, "title" : 1, "year" : 1}
                    )
                    for x in reference_result:
                        print(x)

            elif option == 2:
                return

            else:
                error_msg("Error: Invalid input")
                
    def select_author(self, db, dblp, presentable):
        while True:
            print('''
                ==============options=============
                |   [1.Select               ]    |
                |   [2.Back                 ]    |
                ==================================
                ''')

            option = int(input("Enter the choice you would like to select: "))
            if option == 1:
                select = int(input("Enter the index of the item you want to choose: "))
                if select>len(presentable) or select<=0:
                    error_msg("Error: Invalid input")
                else:
                    print("=========Get more information=========")
                    selected_id = presentable[select - 1]["_id"]
                    select_result = dblp.find(
                        {"authors" : selected_id}, 
                        {"_id" : 0, "title" : 1, "year" : 1, "venue" : 1}
                        ).sort("year", pymongo.ASCENDING)
                    for x in select_result:
                        print(x)
                    
            elif option == 2:
                return

            else:
                error_msg("Error: Invalid input")
          
    def add_article(self):
       while True:
            print("NOTE: separate author names by commas, no spaces")
            inputlist = ["id", "title", "year", "authors"]
            results = [0,0,0,0]
            flag = 0
            for i in range(4):
                string = inputlist[i] + " of the article: "
                invalue = input(string)
                if (len(invalue) == 0):
                    print("Invalid entry,")
                    u = input("press a to try again, or anything to exit: ")
                    if (u == "a"):
                        flag = 1
                        break 
                    else:
                        flag = 2 
                        break

                results[i] = invalue

            if (flag == 1):
                continue
            elif (flag == 2):
                break

            results[3] = results[3].split(",")

            ndoc = {}
            testdoc = {}
            for j in range(4):
                ndoc[inputlist[j]] = results[j] 

            ndoc["abstract"] = None
            ndoc["n_citations"] = 0
            ndoc["references"] = []
            ndoc["venue"] = None

            testdoc = {}
            testdoc[inputlist[0]] = results[0] 
            x = self.dblp.find_one(testdoc)
            if (x != None):
                print("Article is already in database")
                z = input("Type a to insert another article, or anything else to exit: ")
                if (z == "a"):
                    continue
                else:
                    break

            else:
                self.dblp.insert_one(ndoc)
                print("Successfully Added")
                break
       return

      
        
            




