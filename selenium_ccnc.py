from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from datetime import datetime


def get_driver(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options,executable_path=r'geckodriver.exe')
    driver.get(url)
    return driver

def index(driver):
    button = driver.find_elements_by_xpath("""//*[@id="main"]/div[3]/div[3]/form/div[1]/input""")[0]
    button.click()
    nb_page=driver.find_elements_by_xpath("""//*[@id="main"]/div[3]/div[4]""")[0].text
    nb_page=nb_page.split("Page 1/")[1]
    parse_tab(1,nb_page)

def parse_tab(index_depart,nb_page):
    try:
        for i in range(index_depart,int(nb_page)):
            print('page:',i,'/',nb_page)
            page_text = (driver.page_source).encode('utf-8')
            soup = BeautifulSoup(page_text, features="lxml")
            tab = driver.find_elements_by_xpath("""//*[@id="main"]/div[3]/table/tbody/tr""")
            tab.pop(0)
            for row in tab:
                moral_personn = row.find_elements_by_tag_name("td")[0].find_elements_by_tag_name("img")[0].get_attribute("src")
                if "PP" in moral_personn:
                    picto = 'personne morale'
                else:
                    picto='personne physique'
                nom = row.find_elements_by_tag_name("td")[1].text
                lien=row.find_elements_by_tag_name("td")[1].find_elements_by_tag_name("a")[0].get_attribute("href")
                crcc = row.find_elements_by_tag_name("td")[2].text
                cp = row.find_elements_by_tag_name("td")[3].text
                ville = row.find_elements_by_tag_name("td")[4].text
                csv_ligne="{},{},{},{},{},{}\n".format(picto,nom,lien,crcc,cp,ville)
                #print( csv_ligne)
                with open("data.csv", "a") as fichier:
                    fichier.write(csv_ligne)
            button = driver.find_elements_by_xpath("""//*[@id="main"]/div[3]/div[5]/div/a[1]""")[0]
            button.click()
            index_depart=i
    except Exception as e:
       print(e)
       parse_tab(index_depart,nb_page)

if __name__ == "__main__":
    try:
        with open("data.csv", "a+") as fichier:
	            fichier.write("morale/physique,nom,lien,crcc,cp,ville\n")
        firefox_driver = get_driver('http://annuaire.cncc.fr/index.php?page=liste')
        index(firefox_driver)
    except Exception as e:
       print(e)
    finally:
        firefox_driver.close()

