import requests
import datetime
import json

class Newsroom:
    def __init__(self, newsbase:str, keyword: str, sortby: str ):
        
        self.keywords = self.make_query_string(keyword)
        #create todays date to string w/ datetime lib
        self._date = "to=" + (datetime.date.today()).strftime("%Y-%m-%d")
        #get your own API key from newapi.org!!!!!
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self._apikey = "apiKey="
        
        self.newsbase = newsbase
        
        self.sortby = sortby

        #build the url for the requested queries
        self.compile_url()
        #connect to api with url
        self.connection_to_api()
        #do stuff with results
        self.playground()

    def compile_url(self):
        #test url, "iphone", "english", "by popularity"
        #self._news_url = "https://newsapi.org/v2/everything?q=apple&language=en&from=2022-07-16&to=2022-07-16&sortBy=popularity&apiKey="
        self._news_url = f"https://newsapi.org{self.newsbase}{self.keywords}&language=en&{self._date}&{self.sortby}&{self._apikey}"

    def connection_to_api(self):
        #connect to API
        self.news_request = requests.get(self._news_url)
        
        
    def playground(self):
        #json magics
        self.articles = self.news_request.json()['articles']
        self.authors = {article['author'] for article in self.articles}
        self.sources = set([article['source']['id'] for article in self.articles])
        print(f"Found {len(self.articles)} articles")
        print(f"{len(self.authors)} unique authors and {len(self.sources)} unique sources")
        
        results = int(input("How many do you want to see: "))
        if results > len(self.articles) or results<0:
            raise ValueError("Number out of range!")

        for i in range(results):
            print(self.articles[i]['title'].title())
            print("")
            print(self.articles[i]['description'])
            print(f"For more info go to {self.articles[i]['url']}")
            print("")



    def make_query_string(self, keyword):
        if keyword == "":
            return ""
        return "q=" + keyword




#Methods for functional programming
#Asks for searchterms and do error checks
def check_keyword():
    print(f"Only whole dataset supports multiple keyword searches!!!\nLeave field blank if anything goes.")
    search_words = input(f"Use \"\" for exact matching, + if the term must appear: ")
    if len(search_words)>500:
        raise ValueError("Search parameter too long! 500 characters or less!")
    if len(search_words) == 0:
        return ""
    
    phrase_list = search_words.split(" ")
    search_words = ("+").join(phrase_list)
    return search_words

#Ask for which database to search and do error checks.
def check_dataset():
    try:
        data_value = int(input("Search whole dataset (1) or top headlines only (2): "))
    except:
        raise ValueError("Only values 1 or 2 qualify!")
    if data_value != 1 and data_value != 2:
        raise ValueError("Only values 1 or 2 qualify!")


    return ["/v2/everything?", "/v2/top-headlines?"][data_value-1]

    

#which way to sort
def check_sortby():
    try:
        sort_value = int(input("Sort by relevancy (1), popularity (2), new (3): "))
    
    #error in not number
    except:
        raise ValueError("Only values 1-3 qualify!")
    #error wrong numbers
    if 1> sort_value >3:
        raise ValueError("Only values 1-3 qualify!")

    sort_list=["sortBy=relevancy", "sortBy=popularity", "sortBy=publishedAt"]
    return sort_list[sort_value-1] 
    

if __name__ == "__main__":
    #ask for some variables for what news you want to see
    print(f"Hello, what kind of news are you looking for today?")

    #actual API processing
    Newsroom(check_dataset(), check_keyword(), check_sortby())
