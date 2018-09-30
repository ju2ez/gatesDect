from bs4 import BeautifulSoup
import requests
import urllib.request
import re 

hdr = {'User-Agent': 'Mozilla/5.0'}

articleCounter=1
with open("websitesUrlMelinda") as file:
    for url in file:
        try:
            print('Scraping from URL', url)
            req = urllib.request.Request(url,headers=hdr)
            html_page =  urllib.request.urlopen(req).read()
            soup = BeautifulSoup(html_page, 'lxml')
            myDivs = soup.findAll("div", {"class": "article"} )
            myArticle = soup.findAll ("div", {"class":"section-content"})
            article = (myArticle[0].find_all('p'))
            articleFiltered=""
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
                with open("raw_random_articles/article"+str(articleCounter)+"_melinda", 'w+') as f:
                    for item in articleFiltered:
                        f.write("%s " %item)
                articleCounter+=1
        except (KeyboardInterrupt, SystemExit):
             raise
      #  except:
       #     print ("Parsing Error")
