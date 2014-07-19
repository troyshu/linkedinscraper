from linkedin import linkedin


class Person:

    def __init__(self, id, **kwargs):
        self.id = id
        self.firstName = kwargs.pop('firstName', None)
        self.lastName = kwargs.pop('lastName', None)

    def _loadhim_(self):
        profile = li_connection.getProfile(self.id)
        for k, v in profile.iteritems():
            setattr(self, k, v)

class LIScraper:


    def __init__(self):
        # create auth obj
        self.authentication = linkedin.LinkedInDeveloperAuthentication("77b5cimkmbwtcx", "p0AZNOb6OSv5zmZe", "1b0ee31e-3e3a-4688-ba37-5171633b112a", "8b295ec8-3c40-4464-82ed-2dc1054a94c2", "http://localhost:8000", linkedin.PERMISSIONS.enums.values())

        # create application obj
        self.application = linkedin.LinkedInApplication(self.authentication)

    def getAuthenticationObj(self):
        return self.authentication

    def getProfile(self, id):
        return self.application.get_profile(member_id=id)

    def getAllConnections(self):
        return self.application.get_connections()['values']

    def getConnectionsSelectors(self, selectorList):
        return self.application.get_connections(selectors = selectorList)['values']


    def _getKeywordsInText(self, text, keywords):
        '''
            check if a keyword is in some text, given a list of keywords
        '''
        for keyword in keywords:
            if keyword in text:
                return True
        return False

    def getConnectionsWithCurrentPosition(self, positionKeywords):
        '''
            get connections with relevant current position, passing in a list of keywords that should appear in the current position title
        '''

        people = self.getConnectionsSelectors(['id', 'first-name', 'last-name', 'positions'])

        peopleWeWant = []

        for person in people:
            # some people have private profiles
            if 'private' in person.values():
                continue
            positions = person['positions']['values']
            for position in positions:
                if position['isCurrent']:
                    # check if any of our keywords are in current position title
                    foundit = self._getKeywordsInText(position['title'], positionKeywords)

                    if foundit:
                        # if it is, append person obj to the list of people we want to return
                        personObj = Person(
                            id = person['id'],
                            firstName = person['firstName'],
                            lastName = person['lastName'],
                            company = position['company'],
                            title = position['title']
                        )
                        peopleWeWant.append(personObj)


        return peopleWeWant

li_connection=LIScraper()

