#!/usr/bin/python

import threading
import time
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
from selenium_fiche_thread import get_fiches


class myThread (threading.Thread):
    def __init__(self, threadID, index, index_fin):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.index = index
        self.index_fin = index_fin
        self.file_name="data_{}.csv".format(str(self.threadID))

    def run(self):
        init_parse(self.index,self.file_name,self.index_fin,self.threadID)
        raw_data = pd.read_csv(file_name)
        clean_data = raw_data.drop_duplicates()
        clean_data.to_csv("clean_"+self.file_name)

def get_driver(url,index):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options,executable_path=r'geckodriver.exe')
    #driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get(url)
    #time.sleep(1)
    button = driver.find_elements_by_xpath("""//*[@id="main"]/div[3]/div[3]/form/div[1]/input""")[0]
    button.click()
    #time.sleep(1)
    driver.get("http://annuaire.cncc.fr/index.php?page=liste&p={}&tri=rs&ordre=asc".format(str(index)))
    return driver

def parse_tab(driver,index,file_name,index_fin,threadID):
    try:
        for i in range(index,index_fin+1):
            print('page:',index,'/',index_fin)
            page_text = (driver.page_source).encode('utf-8')
            soup = BeautifulSoup(page_text, features="lxml")
            tab = driver.find_elements_by_xpath("""//*[@id="main"]/div[3]/table/tbody/tr""")
            tab.pop(0)
            for row in tab:
                moral_personn = row.find_elements_by_tag_name("td")[0].find_elements_by_tag_name("img")[0].get_attribute("src")
                if "PP" in moral_personn:
                    picto = 'personne physique'
                else:
                    picto='personne morale'
                nom = row.find_elements_by_tag_name("td")[1].text
                lien=row.find_elements_by_tag_name("td")[1].find_elements_by_tag_name("a")[0].get_attribute("href")
                crcc = row.find_elements_by_tag_name("td")[2].text
                cp = row.find_elements_by_tag_name("td")[3].text
                ville = row.find_elements_by_tag_name("td")[4].text
                csv_ligne="{},{},{},{},{},{}\n".format(picto,nom,lien,crcc,cp,ville)
                #print( csv_ligne)
                with open(file_name, "a") as fichier:
                    fichier.write(csv_ligne)
            #time.sleep(2)
            button = driver.find_elements_by_xpath("""//*[@id="main"]/div[3]/div[5]/div/a[1]""")[0]
            button.click()
            index=index+1
    except Exception as e:
        print(e)
        parse_tab(driver,index,file_name,index_fin,threadID)

def init_parse(index,file_name,index_fin,threadID):
    try:
        # with open(file_name, "w+") as fichier:
        #         fichier.write("morale/physique,nom,lien,crcc,cp,ville\n")
        firefox_driver = get_driver("http://annuaire.cncc.fr/index.php?page=liste",index)
        parse_tab(firefox_driver,index,file_name,index_fin,threadID)
    except Exception as e:
        print(e)
    finally:
        firefox_driver.close()

if __name__ == "__main__":
    # Create new threads
    thread1 = myThread(threadID=1, index=1, index_fin=308)
    thread2 = myThread(threadID=2, index=309, index_fin=617)
    thread3 = myThread(threadID=3, index=618, index_fin=925)
    thread4 = myThread(threadID=4, index=926, index_fin=1234)

    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    while thread1.is_alive() and thread2.is_alive() and thread3.is_alive() and thread4.is_alive():
        pass
    get_fiches()

    print( "Exiting Main Thread")