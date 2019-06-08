

class DomainGetter(object):

    __slots__ = ['domain']

    def __init__(self, domain):
        self.domain = domain

    def get_host(self):
        return self.domain
