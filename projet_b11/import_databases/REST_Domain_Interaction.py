from configuration.configuration_api import ConfigurationAPI
from rest_client.AuthenticationRest import AuthenticationAPI
from rest_client.DomainRest import DomainAPI
from rest_client.DomainInteractionPairRest import DomainInteractionPairAPI
from projet_b11.import_databases.Domain_Interaction import DomainInteraction
"""
Date: le 24/04/19

"""

#https://www.tutorialspoint.com/python/python_dictionary.htm
#https://www.journaldev.com/23232/python-add-to-dictionary
#For the uses of dictionnary

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
