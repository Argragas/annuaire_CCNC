#!/usr/bin/python

import threading
import time
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from datetime import datetime


class myThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.file_name="data_{}.csv".format(str(self.threadID))

    def run(self):
        with open(self.file_name,'w+') as writer:
            writer.write("morale/physique,nom,lien,crcc,cp,ville,adresse,tel,fax,mail,insciption,numero_inscription,site_web,forme_juridique,agree_par,reseau,compagnie_regionale,president,vice_president,vice_president_delegue,secretaire,tresorier,membre_bureau,autre_membre_conseil_regional,president_honoraires\n")
        init_parse(self.file_name)

def get_driver(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options,executable_path=r'geckodriver.exe')
    #driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get(url)
    return driver

def init_parse(file_name):
    try:
        firefox_driver = get_driver("http://www.google.fr")
        with open("clean_"+file_name,'r') as reader:
            lines=reader.readlines()
        lines.pop(0)
        print('nb lignes',len(lines))
        for line in lines:
            line_tab=line.split(",")
            is_moral= line_tab[0]
            print("ismoral",is_moral,"lien",line_tab[2])
            
            with open(file_name,'a') as writer:
                if is_moral == "personne morale":
                    writer.write("{},{}\n".format(line.replace("\n",""),get_fiche_morale(firefox_driver,line_tab[2])))
                else:
                    writer.write("{},{}\n".format(line.replace("\n",""),get_fiche_physique(firefox_driver,line_tab[2])))
        firefox_driver.close()
    except Exception as e:
        print(e)


def get_fiche_morale(driver,url):
    try:
        driver.get(url)
        page_text = (driver.page_source).encode('utf-8')
        soup = BeautifulSoup(page_text, features="lxml")
        tab = driver.find_elements_by_xpath("""//*[@id="main"]/div[3]/div[5]/table/tbody/tr""")
        valeur=""
        tab.pop(0)
        for row in tab:
            if ">> Acc" in row.find_elements_by_tag_name("td")[0].text:
                lien = row.find_elements_by_tag_name("td")[0].find_elements_by_tag_name("a")[0].get_attribute("href")
                compagnie=row.find_elements_by_tag_name("td")[0].text.split(" >> Acc")[0]
                valeur="{},{}".format(valeur,lien)
                #valeur="{},{},{}".format(valeur,compagnie,get_fiche_compagnie_regionale(driver,lien))
            else:
                 valeur="{},{}".format(valeur,row.find_elements_by_tag_name("td")[0].text.replace("\n"," ").replace(","," "))
        print(valeur)             
        return valeur[1:]
            
          
    except Exception as e:
        print(e)
        pass
    
def get_fiche_physique(driver,url):
    #,adresse,tel,fax,mail,insciption,numero_inscription,site_web,forme_juridique,agree_par,reseau,compagnie_regionale
    try:
        driver.get(url)
        page_text = (driver.page_source).encode('utf-8')
        soup = BeautifulSoup(page_text, features="lxml")
        tab = driver.find_elements_by_xpath("""//*[@id="main"]/div[3]/div[5]/table/tbody/tr""")
        valeur=""
        tab.pop(0)
        for row in tab:
            if ">> Acc" in row.find_elements_by_tag_name("td")[0].text:
                lien = row.find_elements_by_tag_name("td")[0].find_elements_by_tag_name("a")[0].get_attribute("href")
                compagnie=row.find_elements_by_tag_name("td")[0].text.split(" >> Acc")[0]
                valeur="{},,,{}".format(valeur,lien)
                #valeur="{},{},{}".format(valeur,compagnie,get_fiche_compagnie_regionale(driver,lien))
            else:
                    valeur="{},{}".format(valeur,row.find_elements_by_tag_name("td")[0].text.replace("\n"," ").replace(","," "))
        print(valeur)             
        return valeur[1:]   
    except Exception as e:
        print(e)
        pass

def get_fiche_compagnie_regionale(driver,url):
        driver.get(url)
        page_text = (driver.page_source).encode('utf-8')
        soup = BeautifulSoup(page_text, features="lxml")
        tab = driver.find_elements_by_xpath("""//*[@id="main"]/div[3]/div[6]/table[1]/tbody/tr""")
        valeur=""
        tab.pop(0)
        for row in tab:
            if ">> Acc" in row.find_elements_by_tag_name("td")[0].text:
                lien = row.find_elements_by_tag_name("td")[0].find_elements_by_tag_name("a")[0].get_attribute("href")
                valeur="{},{}".format(valeur,get_fiche_compagnie_regionale(driver,lien))
            else:
                 valeur="{},{}".format(valeur,row.find_elements_by_tag_name("td")[0].text.replace("\n"," ").replace(","," "))
        print(valeur)             
        return valeur[1:]


def get_fiches():
    # Create new threads
    thread1 = myThread(threadID=1)
    thread2 = myThread(threadID=2)
    thread3 = myThread(threadID=3)
    thread4 = myThread(threadID=4)

    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    print( "Exiting Main Thread fiche ")