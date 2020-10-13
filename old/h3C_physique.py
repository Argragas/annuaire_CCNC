from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time


def parse_html():  
    entete="nom prenom;n° inscription;CRCC;annee inscription; site internet;adresse;telephone;fax;associé;salarié;exercant"
    req = requests.get("http://www.h3c.org/fiches/Liste%20des%20commissaires%20aux%20comptes%20(personnes%20physiques).html", timeout=None)
    
    print("debut parse soup")
    soup = BeautifulSoup(req.content, features = 'html.parser')
    print("fin parse soup")
    print("decoupage tab")
    tab = soup.find_all('p')
    print(len(tab))
    final_result=""
    personne=''
    associe="["
    salarie="["
    exercant="["

    for p in tab:
        if " de salari" in p.text:
            associe="{}]".format(associe)
            personne="{};{}".format(personne,associe).replace("\n","")
                
        if "exer" in p.text:
            salarie="{}]".format(salarie)
            personne="{};{}".format(personne,salarie).replace("\n","")
        
        if "Inscription" in p.text and len(personne) > 0:
            #entreprise             
            #associé
            if "]" not in associe:
                if len(associe) == 1:
                    associe=associe+p.text.split("Forme juridique :")[0].strip()
                else:
                    associe=associe+"|"+p.text.split("Forme juridique :")[0].strip()   
            #salarié   
            if "]" in associe:
                if len(salarie) == 1:
                    salarie=salarie+p.text.split("Forme juridique :")[0].strip() 
                else:
                    salarie=salarie+"|"+p.text.split("Forme juridique :")[0].strip()  
                
            #exercant
            if "]" in salarie and "]" in salarie:
                if "En qualité d' exerçant" not in p.text:
                    if len(exercant) == 1:
                        exercant=exercant+p.text.split("Statut :")[0].strip()
                    else:
                        exercant=exercant+"|"+p.text.split("Statut :")[0].strip()
                    #exercant=exercant.replace(p.find_elements_by_tag_name("span")[0].text,"").strip()
        
        if "Inscription" in p.text and len(personne) == 0:
            #personne
            decoupe=p.text.split("N° Inscription : ")
            nom=decoupe[0].strip()
            decoupe=decoupe[1].split("CRCC :")
            num_inscription=decoupe[0].strip()
            decoupe=decoupe[1].split("Année d'inscription :")
            ccrc=decoupe[0].strip()
            decoupe=decoupe[1].split("Site internet :")
            annee_inscription=decoupe[0].strip()
            site_internet=decoupe[1].strip()
            personne="{};{};{};{};{}".format(nom,num_inscription,ccrc,annee_inscription,site_internet).replace("\n","")
            

        if "Adresse professionnelle" in p.text:
            adresse=p.text.replace("Adresse professionnelle","")
            personne="{};{}".format(personne,adresse)
            

        if "Coordonnées téléphoniques" in p.text:
            decoupe=p.text.replace("Téléphone :","").replace("Coordonnées téléphoniques","").split("Fax :")
            tel=decoupe[0].strip()
            fax=decoupe[1].strip()
            personne="{};{};{}".format(personne,tel,fax)
            
        
        if "Commission " in p.text:
            if len(personne) > 1:
                exercant="{}]".format(exercant)
                personne="{};{}".format(personne,exercant).replace("\n","")
                personne=personne.replace("\n","")
           
            if len(final_result) >0:
                final_result="{}\n{}".format(final_result,personne)
            else:
                final_result="{}\n{}".format(entete,personne)
            
            with open("h3c.csv",'w+') as writer:
                writer.write(final_result+"\n") 
            
            personne=""
            associe="["
            salarie="["
            exercant="["
            #break  
    
if __name__ == "__main__":
    
    parse_html()