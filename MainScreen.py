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

        self.main_screen()
        
    def main_screen(self):
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

            elif option == 2:
                # The user should be able to provide a keyword  and see all authors whose names contain the keyword 
                # (the matches should be case-insensitive). For each author, list the author name and the number of publications.
                #  The user should be able to select an author and see the title, year and venue of all articles by that author. 
                #  The result should be sorted based on year with more recent articles shown first.

            elif option == 3:
                # The user should be able to enter a number n and see a listing of top n venues. For each venue, list the venue, 
                # the number of articles in that venue, and the number of articles that reference a paper in that venue. 
                # Sort the result based on the number of papers that reference the venue with the top most cited venues shown first. 
            
            elif option == 4:
                # The user should be able to add an article to the collection by providing a unique id, a title, a list of authors, 
                # and a year. The fields abstract and venue should be set to null, references should be set to an empty array and 
                # n_citations should be set to zero. 




