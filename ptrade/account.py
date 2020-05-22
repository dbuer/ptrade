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
        self.get_balance_url = account_base_url + \
            "balance?accountType={}&instType={}&realTimeNAV={}"
        self.get_transaction_url = account_base_url + \
            "transactions?marker={}&count={}"
        self.get_portfolio_url = account_base_url + "portfolio"
    
    def get_balance(self, realTime=False):
        """ Get the current account balance. 
            TODO: Parse the response. """

        self.accountUser.check_auth()

        balance_url = self.get_balance_url.format(self.accountType, 
            self.institutionType, realTime)

        response = self.accountUser.oauth.get(balance_url)
        return response.text
    
    def get_transactions(self, start=0, count=50):
        """ Get list of COUNT transactions starting at index START. 
            TODO: Add more parameters and parse the response. """

        self.accountUser.check_auth()

        transaction_url = self.get_transaction_url.format(start, count)

        response = self.accountUser.oauth.get(transaction_url)
        return response.text

    def get_portfolio(self):
        """ Get the current account's portfolio.
            TODO: Add more parameters and parse the response. """
        
        self.accountUser.check_auth()

        response = self.accountUser.oauth.get(self.get_portfolio_url)
        return response.text


