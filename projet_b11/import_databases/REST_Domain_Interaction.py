from configuration.configuration_api import ConfigurationAPI
from rest_client.AuthenticationRest import AuthenticationAPI
from rest_client.DomainRest import DomainAPI
import json
from rest_client.DomainInteractionPairRest import DomainInteractionPairAPI
from projet_b11.import_databases.Domain_Interaction import DomainInteraction
"""
Date: le 24/04/19

"""

# https://www.tutorialspoint.com/python/python_dictionary.htm
# https://www.journaldev.com/23232/python-add-to-dictionary
# For the uses of dictionary

# TODO ajouter le systeme de source de db (Dans le JSON?)

"""
Class uses to get information from Inphinity database through the REST API.
This class is used to represent domain-domain interaction and a dictionary of all domain
"""


class RESTDomainInteraction:

    def __init__(self):
        self.domain_dict = {}
        self.domain_interactions = set()
        self.conf = ConfigurationAPI()
        self.conf.load_data_from_ini()
        self.new_domain = set()
        AuthenticationAPI().createAutenthicationToken()

    """
   Function used to get all the domain from inph database with REST and put them in a dictionary.
    """
    def get_domain_dict(self):
        domains = DomainAPI().get_all()
        for domain in domains:
            self.domain_dict.update({domain["id"]: domain["designation"]})

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
            self.domain_interactions.add(DomainInteraction(domain_a, domain_b))

    """
    Function used to find if all Pfam in a set are present in the inphinity database.
    
    :param set_interaction: All new interactions with potential new domain
    
    :type set_interaction: set - required
    
    
    """

    def find_new_domain(self, set_interaction):
        # TODO voir comment on compte insert pour crée le bon format du json
        for interact in set_interaction:
                if interact.first_dom not in self.domain_dict and interact.second_dom not in self.new_domain:
                    self.new_domain.update({interact.first_dom})
                if interact.second_dom not in self.domain_dict and interact.second_dom not in self.new_domain:
                    self.new_domain.update({interact.second_dom})

    "Function used to insert all new Pfam to the database"
    def new_domain_to_json(self):
        domain_list = list()
        for pfam in self.new_domain:
            domain_list.append({"designation": pfam})
        json_data = json.dumps(domain_list)
        print(json_data)


    """
    Function used to put the new interactions in the correct JSON format.

    :param set_interaction: All new interactions

    :type set_interaction: set - required


    """
    def new_interaction_to_json(self, set_interaction):
        interactions_list = list()
        for interact in set_interaction:
            interactions_list.append({"PfamA": interact.first_dom, "PfamB": interact.second_dom})
        print(json.dumps(interactions_list))
