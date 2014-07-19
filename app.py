from linkedin import linkedin


class Person:

    def __init__(self, id, **kwargs):
        self.id = id
        self.firstName = kwargs.pop('firstName', None)
        self.lastName = kwargs.pop('lastName', None)

    def addCompany(self, company):
        # company dictionary
        self.company = company

    def addTitle(self, title):
        self.title = title


    def __repr__(self):
        if hasattr(self, 'title'):
            return u"%s %s %s" % (self.firstName, self.lastName, self.title)
                
        return u"%s %s" % (self.firstName, self.lastName)

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
            print 'checking positions for %s %s' % (person['firstName'], person['lastName'])
            # some people have private profiles
            if 'private' in person.values():
                continue
            prepositions = person['positions']
            # some people don't have positions
            if prepositions['_total'] == 0:
                continue
            else:
                positions = prepositions['values']

            for position in positions:
                if position['isCurrent']:
                    # so many edge cases: some positions don't have titles...
                    if 'title' not in position.keys():
                        continue

                    # check if any of our keywords are in current position title
                    foundit = self._getKeywordsInText(position['title'].lower(), positionKeywords)

                    if foundit:
                        print 'found a potential engineer...'
                        # if it is, append person obj to the list of people we want to return
                        personObj = Person(person['id'], firstName = person['firstName'], lastName = person['lastName'])
                        personObj.addCompany(position['company'])
                        personObj.addTitle(position['title'])

                        peopleWeWant.append(personObj)


        return peopleWeWant



# troy's test
test = LIScraper()
people = test.getConnectionsWithCurrentPosition(['developer', 'quant', 'software engineer', 'programmer'])
for person in people:
    print unicode(person)

