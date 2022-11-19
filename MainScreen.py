import sys
import pymongo
import uuid

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
                    self.article_search_result = []
                    return

                self.article_page = 0
                keywords = set(text.split(' '))

                # l1 = dblp.find({"$and" : [{"title" : { "$regex" : ".*s.*" }}]})
                # for x in l1:
                #     print(x)

                query_word_list = ["title", "authors", "abstract", "venue"]
                where = []
                presentable = []

                for query_word in query_word_list:
                    for keyword in keywords:
                        if keyword == " " or keyword == '':
                            continue
                        
                        search_word = "(?i)^.*?" + keyword + ".*?$"
                        query_segment = {query_word : {"$regex" : search_word } }
                        where.append(query_segment)

                    if len(where) == 0:
                        return

                    result = {"$and" : where}
                    result_list = dblp.find(result, {"_id" : 0, "id" : 1, "title" : 1, "year" : 1, "venue" : 1})

                    exist_flag = False
                    for i in result_list:
                        for j in presentable:
                            if i["id"] == j["id"]:
                                exist_flag = True
                        
                        if (exist_flag == False):
                            presentable.append(i)
                        exist_flag = False
                        
                    where = []
                
                try:
                    keyword_year = int(keywords.pop())
                    result_year_list = dblp.find({"year" : {"$eq" : keyword_year}}, {"_id" : 0, "id" : 1, "title" : 1, "year" : 1, "venue" : 1})
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
       

                for x in presentable:
                    print(x)

                self.select_article(db, dblp, presentable)


            # elif option == 2:
            #     # The user should be able to provide a keyword  and see all authors whose names contain the keyword 
            #     # (the matches should be case-insensitive). For each author, list the author name and the number of publications.
            #     #  The user should be able to select an author and see the title, year and venue of all articles by that author. 
            #     #  The result should be sorted based on year with more recent articles shown first.

            # elif option == 3:
            #     # The user should be able to enter a number n and see a listing of top n venues. For each venue, list the venue, 
            #     # the number of articles in that venue, and the number of articles that reference a paper in that venue. 
            #     # Sort the result based on the number of papers that reference the venue with the top most cited venues shown first. 
            
            # elif option == 4:
            #     # The user should be able to add an article to the collection by providing a unique id, a title, a list of authors, 
            #     # and a year. The fields abstract and venue should be set to null, references should be set to an empty array and 
            #     # n_citations should be set to zero. 

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


        
        
            




