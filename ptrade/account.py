import xmltodict

class Account(object):
    """ Account represents a single trading account owned by a user. """ 

    def __init__(self, accountId, accountIdKey, accountMode, accountDesc, accountName, 
                accountType, institutionType, accountStatus, closedDate, accountUser):
        self.accountId = accountId
        self.accountIdKey = accountIdKey
        self.accountMode = accountMode
        self.accoundDesc = accountDesc
        self.accountName = accountName
        self.accountType = accountType
        self.institutionType = institutionType
        self.accountStatus = accountStatus
        self.closedDate = closedDate
        self.accountUser = accountUser
        account_base_url = self.accountUser.api_base_url + \
            "accounts/{}/".format(self.accountIdKey)
        self.balances_url = account_base_url + "balance"
        self.transactions_url = account_base_url + "transactions"
        self.trans_details_url = self.transactions_url + "/{}"
        self.portfolio_url = account_base_url + "portfolio"
    
    def get_balances(self, realTime=False):
        """ Get the current account balances. """

        self.accountUser.check_auth()

        params = {"accountType": self.accountType, "instType": self.institutionType,
            "realTimeNAV": realTime }

        response = self.accountUser.oauth.get(self.balances_url, params=params)
        response.raise_for_status()
        return xmltodict.parse(response.text)
    
    def list_transactions(self, start=0, count=50, sortOrder='ASC'):
        """ Get list of COUNT transactions starting at index START. """

        self.accountUser.check_auth()

        params = {"marker": start, "count": count, "sortOrder": sortOrder}

        response = self.accountUser.oauth.get(self.transactions_url, params)
        response.raise_for_status()
        return xmltodict.parse(response.text)

    def get_transaction_details(self, tranid):
        """ Get more details about the specified transaction. """

        self.accountUser.check_auth()

        get_transaction_url = self.trans_details_url.format(tranid)

        response = self.accountUser.oauth.get(get_transaction_url)
        response.raise_for_status()
        return xmltodict.parse(response.text)

    def get_portfolio(self):
        """ Get the current account's portfolio. """
        
        self.accountUser.check_auth()

        response = self.accountUser.oauth.get(self.portfolio_url)
        response.raise_for_status()
        return xmltodict.parse(response.text)


