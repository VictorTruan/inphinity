from ftplib import FTP
import gzip
import array
import shutil
import os
import re
# TODO Trouver un format pour pour interaction.
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
        self.interactions = []

    # Méthode permettant d'obtenir la version de la base Pfam, elle est écrite dans un fichier version.txt
    # L'attribut version est utilisé pour stocker la version sous la forme d'un double.
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

    # Méthode permettant d'obtenir toutes les interactions présente dans la base de donnée Pfam.
    # https://bytes.com/topic/python/answers/870172-python-search-text-file-string-replace
    # Pour l'utilisation de fileInput.
    # https://docs.python.org/2/library/fileinput.html
    def get_interactions(self):
        # Telechargement de l'archive
        self.ftp.retrbinary("RETR /pub/databases/Pfam/current_release/database_files/pfamA_interactions.txt.gz",
                            open("./tmp.gz", "wb").write)
        # Ouverture de l'archive
        with gzip.open("./tmp.gz", 'rb') as f_in:
            with open('interactions_pfam.txt', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        # Suppression de l'archive
        os.remove("./tmp.gz")
        interactions = open('interactions_pfam.txt', 'rb')
        # Lecture du fichier par lignes.
        for line in interactions.readlines():
            # Separation des deux domaines d'une interaction
            line = line.decode('UTF-8')
            sep = line.partition('\t')
            sep[2].strip('\n')
            # Creation de l'intéraction et àjout à une liste
            self.interactions.append(Interaction(sep[0], sep[2]))
        # Rangement des intéractions trouvées
        self.interactions =  sorted(self.interactions, key=lambda inter: (inter.premier_dom+inter.second_dom))

    def __str__(self):
        tmp = "Version : " + self.version + "\n Liste des intéractions:\n"
        for inter in self.interactions:
            tmp += inter.__str__()
        return tmp


class Interaction:

    def __init__(self, premier_dom, second_dom):
        self.premier_dom = premier_dom
        self.second_dom = second_dom

    # https://www.dimagi.com/blog/overriding-equals-in-python/ Pour comment redéfinir equals
    def __eq__(self, obj):
        return isinstance(obj, Interaction) and self.premier_dom == obj.premier_dom and\
               self.second_dom == obj.second_dom

    # Méthode pour afficher les domaines présent dans une intéraction
    def __str__(self):
        tmp = "Premier domaine : "+ self.premier_dom + "\nSecond domaine : "+ self.second_dom
        return tmp


fam = pfam()
fam.get_version()
fam.get_interactions()
print(fam)
