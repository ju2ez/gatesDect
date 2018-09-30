from bs4 import BeautifulSoup
import requests
import urllib.request
import re 

hdr = {'User-Agent': 'Mozilla/5.0'}

articleCounter=1
with open("websitesUrlOther") as file:
    for url in file:
        try:
            print('Scraping from URL', url)
            req = urllib.request.Request(url,headers=hdr)
            html_page =  urllib.request.urlopen(req).read()
            soup = BeautifulSoup(html_page, 'lxml')
            myArticle = soup.findAll ("table")
            article = (myArticle[0].find_all('p'))
            for i in range (1,len(myArticle)):
                article += (myArticle[i].find_all('p'))
            articleFiltered=""
            print (articleFiltered)
            for element in article:
                for word in element:
                    myStr = str(word)
                    if "<" in myStr:
                        word="LINK "   
                    articleFiltered+=str(word)
            if len(articleFiltered)>10:
                #Use regular expressions to only include words.
                articleFiltered = re.sub("[^a-zA-Z]"," ", articleFiltered)
              #  articleFiltered=re.sub("[ ,.-;:/\"]", " ", articleFiltered)
                #Convert words to lower case and split them into sperate words.
                articleFiltered = articleFiltered.lower().split()
                with open("raw_random_articles/article"+str(articleCounter), 'w+') as f:
                    for item in articleFiltered:
                        f.write("%s " %item)
                articleCounter+=1
        except (KeyboardInterrupt, SystemExit):
             raise
        except:
            print("Error Parsing")
