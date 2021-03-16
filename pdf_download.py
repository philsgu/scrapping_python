import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep

def askurl():
    askurl = input ("Enter URL: ")
    #create a folder location to save
    folder_location = '/Users/phillipkim/Desktop/webscraping'
    if not os.path.exists(folder_location):
        os.mkdir(folder_location)

    try:
        response = requests.get(askurl, stream=True)
        soup= BeautifulSoup(response.text, "html.parser")  
        #wrap with tqdm progress bar to know status   
        for link in tqdm(soup.select("a[href$='.pdf']")):
            sleep(0.02)
        #Name the pdf files using the last portion of each link which are unique in this case
            filename = os.path.join(folder_location,link['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(askurl,link['href'])).content)
    except requests.ConnectionError as exception:
        print ("URL does NOT exist on Internet")
        askurl()
    except requests.exceptions.MissingSchema as invalidURL:
        print (invalidURL)
        askurl()

askurl()
    