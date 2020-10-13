#!/usr/bin/python

import threading
import time
import os
import re
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import html


class myThread (threading.Thread):
    def __init__(self, threadID,tab_hr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.file_name="data_{}.csv".format(str(self.threadID))
        self.tab_hr=tab_hr

    def run(self):
        for hr in self.tab_hr:
            p=hr
            final_result=""
            personne=''
            p=p.strip()
            #print(p)
            if len(p) > 0:
                p=p.split(" Forme juridique :",1)
                nom=p[0]
                p=p[1]
                p=p.split("N° Inscription : ")
                forme_jurique=p[0]
                p=p[1]
                p=p.split(" CRCC :",1)
                num_inscription=p[0]
                mail=self.get_mail(num_inscription)
                p=p[1]
                p=p.split(" Année d'inscription :",1)
                ccrc=p[0]
                p=p[1]
                p=p.split("Site internet :",1)
                annee_inscription=p[0]
                p=p[1]
                p=p.split("Siège social",1)
                site_internet=p[0]
                p=p[1]
                p=p.split("Téléphone :",1)
                adresse=p[0]
                p=p[1]
                p=p.split("Fax :")
                tel=p[0]
                p=p[1]
                p=p.split("Liste des associés / actionnaires")
                fax=p[0]


                personne_morale="{};{};{};{};{};{};{};{};{}".format(nom,forme_jurique,num_inscription,mail,ccrc,annee_inscription,site_internet,adresse,tel,fax)
                with open("data_morale_{}.csv".format(self.threadID),'a+', encoding='utf8') as writer:
                    writer.write(personne_morale+"\n")
                            

                #break  
        with open("data_morale_{}.csv".format(self.threadID),"r", encoding='utf8') as infile, open("clean_data_morale_{}.csv".format(self.threadID), 'w+', encoding='utf8') as outfile:
            for line in infile:
                if not line.strip(): continue  # skip the empty line
                outfile.write(line)  # non-empty line. Write it to output
        print("fin thread fiche {} : {}".format(self.threadID,datetime.now()))
    
    def get_mail(self,id):
        try:
            url="http://annuaire.cncc.fr/index.php?page=fiche&id={}".format(id.strip())
            
            page = requests.get(url)
            page=page.text
            if """<a href="#" onclick="envoi_mel(this.innerHTML);">""" in page:
                page=page.split("""<a href="#" onclick="envoi_mel(this.innerHTML);">""")[1]
                page= page.split("</a>")[0]
            else:
                page=""
            return page.replace("[arrobase]","@")
        except Exception as e:
            print(id)
            print(e)
            pass
        
