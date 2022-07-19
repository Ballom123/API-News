import requests
import datetime
import json

class Newsroom:
    def __init__(self, keyword: str, date: datetime, lang: str, newsbase:int, sortby: int ):
        
        
        self.keywords = "q=" + keyword
        self.language = "language=" + lang
        self.date = "to=" + date.strftime("%Y-%m-%d")
        #Get your own API key from newsapi.org!
        self._apikey = "apiKey="

        if newsbase == 1:
            self.newsbase = "/v2/everything?"
        elif newsbase == 2:    
            self.newsbase= "/v2/top-headlines?"
        
        if sortby == 1:
            self.sortby= "sortBy=relevancy"
        elif sortby == 2:
            self.sortby= "sortBy=popularity"
        elif sortby == 3:
            self.sortby= "sortBy=publishedAt"

        #build the url for the requested queries
        self.compile_url()
        #connect to api with url
        self.connection_to_api()

    def compile_url(self):
        #test url, "iphone", "english", "by popularity"
        #self.news_url = "https://newsapi.org/v2/everything?q=apple&language=en&from=2022-07-16&to=2022-07-16&sortBy=popularity&apiKey="
        self.news_url = f"https://newsapi.org{self.newsbase}{self.keywords}&{self.language}&{self.date}&{self.sortby}&{self._apikey}"

    def connection_to_api(self):
        #connect to API
        self.news_request = requests.get(self.news_url)
        #json magics happen
        self.response = self.news_request.json()
        self.articles = self.response["articles"]
        #ask for how many to see
        print(f"Found {len(self.articles)} articles")
        results = int(input("How many do you want to see: "))
        if results > len(self.articles) or results<0:
            raise ValueError("Number out of range!")

        for i in range(results):
            print(self.articles[i]['title'].title())
            print("")
            print(self.articles[i]['description'])
            print(f"For more info go to {self.articles[i]['url']}")
            print("")




if __name__ == "__main__":
    #ask for some variables for what news you want to see
    #keyword, date, language, source domain
    print(f"Hello, what kind of news are you looking for?")
    print(f"Leave field blank if anything goes")
    news_words = input(f"Keywords in article\nUse \"\" for exact match, + if must appear: ")
    news_date = datetime.date.today()
    news_lang = input(f"Choose a language\nar, de, en, es, fr, he, it, nl, no, pt, ru, sv, ud, zh: ")
    if news_lang not in ["ar", "de", "en", "es", "fr", "he", "it", "nl", "no", "pt", "ru", "sv", "ud", "zh"]:
        raise ValueError("Language not from list!")
    news_top_or_not = int(input("Whole dataset (1) or top headlines (2): "))
    if news_top_or_not != 1 and news_top_or_not != 2:
        raise ValueError("Only values 1 or 2 qualify!")
    news_sort = int(input("Sort by relevancy (1), popularity (2), new (3): "))
    if 1> news_sort >3:
        raise ValueError("Only values 1-3 qualify!")

    #Test variables
    #news_words = "iphone"
    #news_date = ""
    #news_lang = "english"
    #news_top_or_not = 2
    
    #actual API processing
    Newsroom(news_words, news_date, news_lang, news_top_or_not, news_sort)
