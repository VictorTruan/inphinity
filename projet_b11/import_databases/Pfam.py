from ftplib import FTP
import gzip
import shutil
import os
import re
# TODO Trouver un format pour pour ineraction.
# TODO Ouvrir la connexion avec la base de donnée inphinity
# TODO Utiliser REST pour récuperer toutes les intéractions.
# TODO Récuperer toutes les interactions sur le serveur FTP
# TODO Mettre les interaction inphinity au bon format
# TODO Mettre les interactions Pfam au bon format
# TODO Comparer les resultats.
# Dans un second temps
# TODO Si différente
    # TODO Trouver les diff et les insérer avec REST
    # TODO Passer toutes les prot a HMM
    # TODO Trier tous les domaine de REST et HMM afin de trouver les nouveaux et les insérers
    # TODO Lancer les nouveaux calcules de scores.
# TODO Sinon
    #TODO Pas grand chose pour le moment.
#TODO Trouver comment lancer automatiquement une maj.

class pfam:

    server_adress = 'ftp.ebi.ac.uk'

    def __init__(self):
        self.version = None
        self.ftp = FTP(self.server_adress)
        self.ftp.login()

    # Méthode permettant d'obtenir la version de la base Pfam, elle est écrite dans un fichier version.txt
    # L'attribut version est utilisé pour stocker la version sous la forme d'un double.
    def get_version(self):
        self.ftp.retrbinary("RETR /pub/databases/Pfam/current_release/Pfam.version.gz", open("./tmp.gz", "wb").write)
        with gzip.open("./tmp.gz", 'rb') as f_in:
            with open('version.txt', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove("./tmp.gz")
        self.version = open('./version.txt','r').read()
        self.version = re.findall('\d+.\d+', self.version)[0]
        print(self.version)


fam = pfam()
fam.__init__()
fam.get_version()
