from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import re
import os
from h3c_thread_morale import myThread


def parse_html():  
    entete="nom prenom;n° inscription;CRCC;annee inscription; site internet;adresse;telephone;fax;associé;salarié;exercant"
    req = requests.get("http://www.h3c.org/fiches/Liste%20des%20commissaires%20aux%20comptes%20(personnes%20morales).html", timeout=None)
    req_text=req.text
    
    req_text=req_text.replace("<html>","")
    req_text=req_text.replace("</html>","")
    req_text=req_text.replace("</p>","")
    req_text=req_text.replace("</br>","")
    req_text=req_text.replace("<br/>","")
    req_text=req_text.replace("<b>"," ")
    req_text=req_text.replace("</b>"," ")
    req_text=req_text.replace("&nbsp;","")
    req_text=req_text.replace("""<span style="text-decoration : underline;">"""," ")
    req_text=req_text.replace("</span>"," ")
    req_text=req_text.replace("""<span style="font-style : italic;">"""," ")
    req_text=req_text.replace("<p>","")
    req_text=req_text.replace("\n","")
    req_text=p=re.sub(' +', ' ',req_text)
    #print(req_text)
    tab=req_text.split("<hr/>")
    
    print("longueur tab",len(tab))
    chunks = decoupe(tab)
    print("nombre de tab",len(chunks))
    total=0
    for c in chunks:
        total=total+len(c)
    print("verif total chunck",total)
    get_thread(chunks)

def get_date_mise_a_jour():
    req = requests.get("http://www.h3c.org/fiches/Liste%20des%20commissaires%20aux%20comptes%20(personnes%20morales).html", timeout=None)
    soup = BeautifulSoup(req.text)
    date=soup.find(id='bdroite').get_text()
    return date

def decoupe(hr_list):
    n = 4
    num = float(len(hr_list))/n
    l = [ hr_list [i:i + int(num)] for i in range(0, (n-1)*int(num), int(num))]
    l.append(hr_list[(n-1)*int(num):])
    return l


def get_thread(chunks):
    
    threads = []
    # Create new threads
    thread1 = myThread(threadID=1,tab_hr=chunks[0])
    thread2 = myThread(threadID=2,tab_hr=chunks[1])
    thread3 = myThread(threadID=3,tab_hr=chunks[2])
    thread4 = myThread(threadID=4,tab_hr=chunks[3])

    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    threads.append(thread4)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    #Wait for all of them to finish
    for x in threads:
        x.join()
    
    print("debut fusion : {}".format(datetime.now()))
    fusion()
    print("fin fusion : {}".format(datetime.now()))
    for fname in os.listdir("./"):
        if "data" in fname:
            os.remove(os.path.join("./", fname))
    print( "Exiting Main Thread {}".format(datetime.now()))
    
def fusion():
    date_mise_a_jour=get_date_mise_a_jour("http://annuaire.cncc.fr/index.php")
    with open("h3c_morale_{}.csv".format(date_mise_a_jour),'w+', encoding='utf8') as writer:
        writer.write("nom;forme juridique;n° inscription;mail;CRCC;annee inscription;site internet;adresse;telephone;fax\n")
    for i in range(1,5):
        with open("clean_data_morale_{}.csv".format(i),'r', encoding='utf8') as reader:
            lines=reader.readlines()
        with open("h3c_morale.csv",'a', encoding='utf8') as writer:
            writer.writelines(lines)


if __name__ == "__main__":
    
    parse_html()