from ftplib import FTP
import ftplib
from projet_b11.import_databases.Domain_Interaction import DomainInteraction
import gzip
import logging
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
     ##--> Diff trouvée
    # TODO Passer toutes les prot a HMM
    # TODO Trier tous les domaine de REST et HMM afin de trouver les nouveaux et les inserers
    # TODO Lancer les nouveaux calcules de scores.
#TODO Trouver comment lancer automatiquement une maj.

"""
Class used to get domain-domain interaction from Pfam
"""
version_filename = "version.txt"
interaction_filename = "interactions_pfam.txt"


class Pfam:

    def __init__(self):
        self.server_address = 'ftp.ebi.ac.uk'
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.log.addHandler(logging.StreamHandler())
        self.version = None
        try:
            self.log.info("Opening FTP connexion with {}".format(self.server_address))
            self.ftp = FTP(self.server_address)
            self.ftp.login()
        except ftplib.all_errors as e:
            self.log.error('Connexion with FTP does not work.')
            raise e
        self.domain_interactions = set()

    """
    Function used to get the Pfam database version. self.version is used to keep it.
    """
    # http://zetcode.com/python/ftp/ Pour la connexion FTP
    # https://stackoverflow.com/questions/48466421/python-how-to-decompress-a-gzip-file-to-an-uncompressed-file-on-disk
    # Pour l'ouverture du gz.
    def get_version(self):
        try:
            self.log.info("Downloading version file")
            self.ftp.retrbinary("RETR /pub/databases/Pfam/current_release/Pfam.version.gz",
                                open("./tmp.gz", "wb").write)
        except ftplib.all_errors as e:
            self.log.error("Download of the version from iPfam crashed.")
            raise e
        self.log.info("Extracting archive to {}".format(version_filename))
        with gzip.open("./tmp.gz", 'rb') as f_in:
            with open(version_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove("./tmp.gz")
        self.version = open(version_filename, 'r').read()
        self.version = re.findall('\\d+.\\d+', self.version)[0]
        self.log.info("Version is set to {}".format(self.version))
    """
    Function used to get all the domain-domain interactions from Pfam database.
    All the interaction are in domain_interactions
    """
    # https://bytes.com/topic/python/answers/870172-python-search-text-file-string-replace
    # For fileInput.
    # https://docs.python.org/2/library/fileinput.html
    def get_interactions(self):
        # Downloads of the archive
        try:
            self.ftp.retrbinary("RETR /pub/databases/Pfam/current_release/database_files/pfamA_interactions.txt.gz",
                                open("./tmp.gz", "wb").write)
        except ftplib.all_errors as e:
            self.log.error("Download of the interactions from iPfam crashed")
            raise e
        # Opening of the archive
        self.log.info("Extracting archive to {}".format(interaction_filename))
        with gzip.open("./tmp.gz", 'rb') as f_in:
            with open(interaction_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        # Suppression of the archive
        os.remove("./tmp.gz")
        interactions = open(interaction_filename, 'rb')
        # We read the file line by line.
        self.log.info("Reading and creating the interactions ")
        for line in interactions.readlines():
            # Separations of both domain from the interaction
            line = line.decode('UTF-8')
            line = line.strip('\n')
            sep = line.partition('\t')
            # Instantiation of a new interaction and add it to domain_interactions
            self.domain_interactions.add(DomainInteraction(sep[0], sep[2]))
        self.log.info("All Pfam interactions done")
    """
    Redefinition of toString so it display all the interactions in Pfam Database.
    """
    def __str__(self):
        tmp = "Version : " + self.version + "\n List of all interactions:\n"
        for inter in self.domain_interactions:
            tmp += inter.__str__()
        return tmp


# Test
pfam = Pfam()
pfam.get_interactions()
inphi = RESTDomainInteraction()
inphi.get_domain_dict()
inphi.get_domain_inter()
tmp = pfam.domain_interactions - inphi.domain_interactions
print(tmp)
inphi.update_inphinity_database(tmp, "iPfam")
