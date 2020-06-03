import json
from bs4 import BeautifulSoup
import os
def writeToJSONFile(filePath, data):
    with open(filePath, 'a') as fp:
        json.dump(data, fp)
        fp.write("\n")

# The main function, the entry point
if __name__ == '__main__':
    files=os.listdir(r"C:\Users\leoac\Desktop\ChatExport_29_05_2020")
    files.sort()
    for file in files:
        if(file[-4:]=="html"):
            filepath="C:/Users/leoac/Desktop/ChatExport_29_05_2020" + "/"+file
            aOneProductsDescPage = open(filepath, encoding='utf-8')
            aBeautifulSoup = BeautifulSoup(aOneProductsDescPage, features="html.parser")
            aOneProductsDescPage.close()
            history=aBeautifulSoup.find('div',{"class":"history"})
            divs=history.find_all('div',class_="body")
            date=""
            username=""
            text=""
            for div in divs:
                if(div["class"]==['body']):
                    dateDiv=div.find("div", class_="pull_right date details")
                    nameDiv=div.find("div", class_="from_name")
                    textDiv=div.find("div", class_="text")

                    if dateDiv!=None:
                        date=dateDiv["title"]
                    else :
                        continue
                    if nameDiv!=None:
                        username=nameDiv.text.strip()
                    if textDiv != None:
                        text=textDiv.text.strip()
                    else :
                        text="NOT TEXT"


                    aNewMessage={}
                    aNewMessage["date"]=date
                    aNewMessage["username"]=username
                    aNewMessage["text"]=text
                    writeToJSONFile(r"C:\Users\leoac\Desktop\ChatExport_29_05_2020.json", aNewMessage)