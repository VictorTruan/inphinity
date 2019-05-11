from configuration.configuration_api import ConfigurationAPI
from rest_client.AuthenticationRest import AuthenticationAPI
from rest_client.DomainRest import *
from rest_client.DomainInteractionPairRest import *
from rest_client.DomainSourceInformationRest import *
from rest_client.DomainInteractionSourceRest import *
from projet_b11.import_databases.Domain_Interaction import DomainInteraction
import datetime
"""
Date: le 24/04/19

"""
#TODO separer l'insert d'interaction et l'insert d'interaction par bd
#TODO -> Si on la trouve pas AVEC SOURCE on regarde si on la trouve SANS SOURCE
#TODO -> Si on la trouve sans source on l'insert dans les sources
#TODO -> Si on la trouve pas sans les sources on l'insert dans les non-source et les sources.

# https://www.tutorialspoint.com/python/python_dictionary.htm
# https://www.journaldev.com/23232/python-add-to-dictionary
# For the uses of dictionary


"""
Class uses to get information from Inphinity database through the REST API.
This class is used to represent domain-domain interaction and a dictionary of all domain
"""


class RESTDomainInteraction:

    def __init__(self):
        self.domain_dict = dict()  # Dictionnary from id to Pfam
        self.reverse_dict_domain = {}  # Dictionnary from Pfam to id
        self.source_dict = dict()  # Dictionnary Source String to source id
        self.interact_dict = dict()  # Dictionnary from a pair and interact id
        self.interact_dict_reverse = dict()  # Dictionnary from a pair and interact id
        self.domain_interactions = set()  # Set of all interactions
        self.domain_interactions_source = list()  # Set of all interactions with source
        self.conf = ConfigurationAPI()
        self.conf.load_data_from_ini()
        self.new_domain = set()  # Set for all the new domain we need to insert
        AuthenticationAPI().createAutenthicationToken()

    """
   Function used to get all the domain from inph database with REST and put them in a dictionary.
    """
    def get_domain_dict(self):
        domains = DomainAPI().get_all()
        for domain in domains:
            self.domain_dict.update({domain["id"]: domain["designation"]})
            self.reverse_dict_domain.update({domain["designation"]: domain["id"]})

    """
    Function used to get all the domain-domain interactions from inph database with REST and put them in a set.
    """
    def get_domain_inter(self):
        p = DomainInteractionPairAPI()
        interactions = p.get_all()
        for interaction in interactions:
            # Creation of the new interaction
            domain_a = self.domain_dict.get(interaction['domain_a'])
            domain_b = self.domain_dict.get(interaction['domain_b'])
            tmp = DomainInteraction(domain_a, domain_b)
            self.domain_interactions.add(tmp)
            self.interact_dict.update({interaction['id']: tmp})
            self.interact_dict_reverse.update({tmp: interaction['id']})

    def get_inter_source(self):
        p = DomainInteractionSourceAPI()
        interactions = p.get_all()
        for interaction in interactions:
            interact = self.interact_dict_reverse.get(interaction['domain_interaction'])
            self.domain_interactions_source.append({interact, interaction['information_source']})
    """
    Function used to find if all Pfam in a set are present in the inphinity database.
    
    :param set_interaction: All new interactions with potential new domain
    
    :type set_interaction: set - required
    
    
    """
    def find_new_domain(self, set_interaction):
        for interact in set_interaction:
                if interact.first_dom not in self.domain_dict.values() and interact.second_dom not in self.new_domain:
                    self.new_domain.add({interact.first_dom})
                if interact.second_dom not in self.domain_dict.values() and interact.second_dom not in self.new_domain:
                    self.new_domain.add({interact.second_dom})

    "Function used to insert all new Pfam to the database"
    def new_domain_to_data(self):
        domain_list = list()
        for pfam in self.new_domain:
            domain_list.append({"designation": pfam})
        return domain_list

    """
    Function used to put the new interactions in the correct JSON format.

    :param set_interaction: All new interactions

    :type set_interaction: set - required


    """
    def new_interaction_to_data(self, set_interaction):
        interactions_list = list()
        for interact in set_interaction:
            interactions_list.append({"domain_a": self.reverse_dict_domain.values(interact.first_dom), "domain_b":
                self.reverse_dict_domain.values(interact.second_dom)})
        return interactions_list
    """
    Function used to insert all the new interaction, it all the correct format and insert the linked InteractionSource.
    
    :param set_interaction: A set containing all interactions.
    :source: A string which is the database name.
    
    :type set_interaction: set - required
    :type source: String - required
    """
    def insert_new_interaction(self, interact_data, source):
        for interact in interact_data:
            interact_id = DomainInteractionPairAPI().setDomainInteractionPair(interact)
            DomainInteractionSourceAPI().setDomainInteractionSource({"date_creation": datetime.date.today()
                                                                    , "domain_interaction": interact_id
                                                                    , "source": self.source_dict.get(source)})

    """
    Function used to update the inphinity database. It use one set of interaction and one source.
    The function is going to find all new interactions, all new domain from tham and insert the Domain, interactions
    ans interaction source.
    
    :param set_interaction: A set containing all interactions.
    :source: A string which is the database name.
    
    :type set_interaction: set - required
    :type source: String - required
    """
    def update_inphinity_database(self, set_interaction, source):
        #TODO Faire appel a toutes les autres méthodes pour que on puisse utiliser que celle la depuis un nouveau set.

        #TODO Pour le moment on n'a que insert_new_ineraction qui fait l'insert SI l'ineract est nul part, il faut gérer les cas
        #TODO Ou l'interaction et deja présente mais pas dans la table avec la source pour laquelle on recherche.

    """
    Function used during the update to put the new domains in the inphinity database.
    """
    def insert_new_domain(self):
        all_domain = self.new_domain_to_data()
        for domain in all_domain:
            new_id = DomainAPI().setDomain(domain)
            self.domain_dict.update({new_id: domain["designation"]})
            self.reverse_dict_domain.update({domain["designation"]: new_id})

    """
    Function used to create a mapping between the source name and database id.
    """
    def find_all_source(self):
        sources = DomainSourceInformationAPI().get_all()
        for source in sources:
            self.source_dict.update({source["designation"]: source["id"]})
