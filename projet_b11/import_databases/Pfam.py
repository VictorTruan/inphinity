from ftplib import FTP
from projet_b11.import_databases.Domain_Interaction import DomainInteraction
import gzip
import shutil
import os
import re
#TODO import de test
from projet_b11.import_databases.REST_Domain_Interaction import RESTDomainInteraction
import sys
#TODO import de test

# TODO Trouver un format pour pour interaction.
    ##--> Pas de classes sans SQL, creation d'une miniclasse
# TODO Ouvrir la connexion avec la base de donnee inphinity
    ##--> Fait par Nico
# TODO Utiliser REST pour recuperer toutes les interactions.
    ##-->Fait dans Rest_Pfam
# TODO Recuperer toutes les interactions sur le serveur FTP
    ##--> Fait, cette classe permet de retourner
# TODO Mettre les interaction inphinity au bon format
    ##-->Fait la classe contient un set
# TODO Mettre les interactions Pfam au bon format
    ##--> Fait, la classe contient un set.
# TODO Comparer les resultats.
# Dans un second temps
# TODO Si differente
    # TODO Trouver les diff et les inserer avec REST
        #TODO utiliser les set
    # TODO Passer toutes les prot a HMM
    # TODO Trier tous les domaine de REST et HMM afin de trouver les nouveaux et les inserers
    # TODO Lancer les nouveaux calcules de scores.
#TODO Trouver comment lancer automatiquement une maj.

"""
Class used to get domain-domain interaction from Pfam
"""
class Pfam:

    server_adress = 'ftp.ebi.ac.uk'

    def __init__(self):
        self.version = None
        self.ftp = FTP(self.server_adress)
        self.ftp.login()
        self.domain_interactions = set()


    """
    Function used to get the Pfam database version. self.version is used to keep it.
    """
    # http://zetcode.com/python/ftp/ Pour la connexion FTP
    # https://stackoverflow.com/questions/48466421/python-how-to-decompress-a-gzip-file-to-an-uncompressed-file-on-disk
    # Pour l'ouverture du gz.
    def get_version(self):
        self.ftp.retrbinary("RETR /pub/databases/Pfam/current_release/Pfam.version.gz", open("./tmp.gz", "wb").write)
        with gzip.open("./tmp.gz", 'rb') as f_in:
            with open('version.txt', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove("./tmp.gz")
        self.version = open('./version.txt','r').read()
        self.version = re.findall('\d+.\d+', self.version)[0]
    """
    Function used to get all the domain-domain interactions from Pfam database.
    All the interaction are in domain_interactions
    """
    # https://bytes.com/topic/python/answers/870172-python-search-text-file-string-replace
    # For fileInput.
    # https://docs.python.org/2/library/fileinput.html
    def get_interactions(self):
        # Downloads of the archive
        self.ftp.retrbinary("RETR /pub/databases/Pfam/current_release/database_files/pfamA_interactions.txt.gz",
                            open("./tmp.gz", "wb").write)
        # Opening of the archive
        with gzip.open("./tmp.gz", 'rb') as f_in:
            with open('interactions_pfam.txt', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        # Suppression of the archive
        os.remove("./tmp.gz")
        interactions = open('interactions_pfam.txt', 'rb')
        # We read the file line by line.
        for line in interactions.readlines():
            # Separations of both domain from the interaction
            line = line.decode('UTF-8')
            line = line.strip('\n')
            sep = line.partition('\t')
            # Instanciation of a new interaction and add it to domain_interactions
            self.domain_interactions.add(DomainInteraction(sep[0], sep[2]))
    """
    Redefinition of toStringso it display all the interactions in Pfam Database.
    """
    def __str__(self):
        tmp = "Version : " + self.version + "\n List of all interactions:\n"
        for inter in self.domain_interactions:
            tmp += inter.__str__()
        return tmp


#Test
pfam = Pfam()
pfam.get_interactions()
inphi = RESTDomainInteraction()
inphi.get_domain_dict()
inphi.get_domain_inter()
tmp = pfam.domain_interactions - inphi.domain_interactions
print(str(len(pfam.domain_interactions)) + " interactions in pfam database")
print(str(len(inphi.domain_interactions))+ " interactions in inph database")
print(str(len(tmp)) + " interactions in pfam database but not in inph")

for interaction in pfam.domain_interactions:
    if interaction not in inphi.domain_interactions:
        pass
#TODO Insert if missing, move this code to a function
    else:
        pass
