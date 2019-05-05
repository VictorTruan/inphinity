"""
Class used to represent a domain-domain interaction
"""


class DomainInteraction:

    def __init__(self, first_dom, second_dom):
        self.first_dom = first_dom
        self.second_dom = second_dom

    # https://www.dimagi.com/blog/overriding-equals-in-python/ How to define equals.
    """
    Redefine equals so we can compare each domain-domain interaction easily.
    """
    def __eq__(self, obj):
        return isinstance(obj, DomainInteraction) and ((self.first_dom == obj.first_dom and
                                                        self.second_dom == obj.second_dom) or
                                                       (self.first_dom == obj.second_dom and
                                                        self.second_dom == obj.first_dom))
    """
    Override of str 
    """
    def __str__(self):
        return "First domain : " + self.first_dom + "\nSecond domain : " + self.second_dom

    """
    To redefine Hash, we are concatenate the two domain  and hash the result string.
    """
    def __hash__(self):
        if self.first_dom == self.second_dom:
            return hash(self.first_dom)
        return hash(self.first_dom) ^ hash(self.second_dom)
