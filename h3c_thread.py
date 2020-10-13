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
            
            if len(p) > 0:
                p=p.split("N° Inscription :",1)
                nom=p[0]
                p=p[1]
                p=p.split("CRCC :")
                num_inscription=p[0]
                mail=self.get_mail(num_inscription)
                p=p[1]
                p=p.split("Année d'inscription :",1)
                ccrc=p[0]
                p=p[1]
                p=p.split("Site internet :",1)
                annee_inscription=p[0]
                p=p[1]
                p=p.split("Adresse professionnelle",1)
                site_internet=p[0]
                p=p[1]
                p=p.split("Coordonnées téléphoniques Téléphone :",1)
                adresse=p[0]
                p=p[1]
                p=p.split("Fax :",1)
                tel=p[0]
                p=p[1]
                p=p.split("Modalités d'exercice En qualité d'associé")
                fax=p[0]
                p=p[1]
                p=p.split("En qualité de salarié")
                associe=p[0]
                p=p[1]
                p=p.split("En qualité d' exerçant")
                salarie=p[0]
                p=p[1]    
                p=p.split("Commission régionale")
                exercant=p[0]
                t=[]
                t=self.decoupe_exercice(associe,t)
                associe= ",".join(t)
                associe="["+associe+"]"
                t=[]
                t=self.decoupe_exercice(salarie,t)
                salarie= ",".join(t)
                salarie="["+salarie+"]"
                t=[]
                t=self.decoupe_exercice(exercant,t)
                exercant= ",".join(t)
                exercant="["+exercant+"]"

                personne="{};{};{};{};{};{};{};{};{};{};{};{}".format(nom,num_inscription,mail,ccrc,annee_inscription,site_internet,adresse,tel,fax,associe,salarie,exercant)
                with open("data_{}.csv".format(self.threadID),'a+', encoding='utf8') as writer:
                    writer.write(personne+"\n")
                            

                #break  
        with open("data_{}.csv".format(self.threadID),"r", encoding='utf8') as infile, open("clean_data_{}.csv".format(self.threadID), 'w+', encoding='utf8') as outfile:
            for line in infile:
                if not line.strip(): continue  # skip the empty line
                outfile.write(line)  # non-empty line. Write it to output
        print("fin thread fiche {} : {}".format(self.threadID,datetime.now()))
    
    def decoupe_exercice(self,tab_exercice,exercice):
               
        while "Forme juridique :" in tab_exercice or "Statut :" in tab_exercice or len(tab_exercice) > 0:
            tab_exercice=tab_exercice.strip()
            if "www" in tab_exercice.split(' ', 1)[0] or "http" in tab_exercice.split(' ', 1)[0]:
                tab_exercice= tab_exercice.split(' ', 1)
                tab_exercice= tab_exercice[1] if len(tab_exercice) > 1 else ""
            tab_exercice = tab_exercice.split("Site internet :",1)
            if "Forme juridique :" in tab_exercice[0]:
                exercice.append(tab_exercice[0].split("Forme juridique :",1)[0])
            else:
                exercice.append(tab_exercice[0].split("Statut :",1)[0])
            if len(tab_exercice) > 1:
                tab_exercice=tab_exercice[1]
            else:
                tab_exercice=""
        return exercice

    def get_mail(self,id):
        try:
            url="http://annuaire.cncc.fr/index.php?page=fiche&type=pp&id={}".format(id.strip())
            
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
        
