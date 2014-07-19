from linkedin import linkedin


class LIScraper:


    def __init__(self):
        # create auth obj
        self.authentication = linkedin.LinkedInDeveloperAuthentication("77b5cimkmbwtcx", "p0AZNOb6OSv5zmZe", "1b0ee31e-3e3a-4688-ba37-5171633b112a", "8b295ec8-3c40-4464-82ed-2dc1054a94c2", "http://localhost:8000", linkedin.PERMISSIONS.enums.values())

        # create application obj
        self.application = linkedin.LinkedInApplication(self.authentication)

    def getAuthenticationObj(self):
        return self.authentication

    def getAllConnections(self):
        return self.application.get_connections()['values']

    def getConnectionsSelectors(self, selectorList):
        return self.application.get_connections(selectors = selectorList)['values']

