import logging
import enum
import webbrowser
import xmltodict

from requests_oauthlib import OAuth1Session
from oauthlib.common import add_params_to_uri
from .account import Account

ETRADE_LOGIN_URL = "https://us.etrade.com/e/t/etws/authorize"
OAUTH_BASE_URL = "https://api{}.etrade.com/oauth/"
API_BASE_URL = "https://api{}.etrade.com/v1/"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class Environment(enum.Enum):
    sandbox = "sandbox"
    production = "production"

class UserNotAuthenticatedError(Exception):
    """ An error raised when the user tries to make priveleged requests
        without being fully authenticated. """
    
    def __init__(self):
        message = "user is not authenticated."
        super().__init__(message)

class User:
    """ User represents an Etrade user instance. """

    def __init__(self, consumer_key, consumer_secret, production=False, login_url=ETRADE_LOGIN_URL):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.login_url = login_url
        self.oauth_base_url = OAUTH_BASE_URL.format("" if production else "sb")
        self.api_base_url = API_BASE_URL.format("" if production else "sb")
        self.request_token_url = self.oauth_base_url + "request_token"
        self.access_token_url = self.oauth_base_url + "access_token"
        self.renew_token_url = self.oauth_base_url + "renew_access_token"
        self.revoke_token_url = self.oauth_base_url + "revoke_access_token"
        self.list_accounts_url = self.api_base_url + "accounts/list"
        
        if production:
            self.environment = Environment.production
        else:
            self.environment = Environment.sandbox

        log.info(f"Created {self.environment} user")

    @property
    def authenticated(self):
        return self.oauth is not None and self.oauth.authorized

    def login(self):
        """ Starts the OAuth 1.0 lifecycle and gets the user access token.
            The user access token will expire at midnight US Eastern time. """

        self.oauth = OAuth1Session(
            client_key=self.consumer_key, 
            client_secret=self.consumer_secret, 
            callback_uri="oob"
        )

        # Get a request token
        request_token = self._get_request_token()

        # Get the login url
        login_params = { "key": self.consumer_key, "token": request_token }
        authorize_url = add_params_to_uri(ETRADE_LOGIN_URL, login_params)

        # Open the url in default browser
        webbrowser.open(authorize_url, new=2)

        # Get the verification code
        verifier = input("\nEnter verification code: ")

        # Get access token
        return self.oauth.fetch_access_token(self.access_token_url, verifier)

    def logout(self):
        """ Revokes the user access token. Call before terminating application. """
        
        self.check_auth()
        response = self.oauth.get(self.revoke_token_url)
        self.oauth = None
        response.raise_for_status()
        return True

    def renew(self):
        """ Renews the user access token. Access token becomes inactive 
            if your application does not make API requests for two hours. """
        
        self.check_auth()
        response = self.oauth.get(self.renew_token_url)
        response.raise_for_status()
        return True

    def get_all_accounts(self):
        """ Returns a list of accounts for the current user. """

        self.check_auth()
        response = self.oauth.get(self.list_accounts_url)
        response.raise_for_status()
        return self._parse_accounts(response.text)
    
    def get_account_by_name(self, accountName):
        accounts = self.get_all_accounts()
        for account in accounts:
            if account.accountName == accountName:
                return account
        return None
        
    def get_account_by_id(self, accountId):
        accounts = self.get_all_accounts()
        for account in accounts:
            if account.accountId == accountId:
                return account
        return None
    
    def _get_request_token(self):
        """ Request tokens are valid for 5 minutes. """

        request_token_response = self.oauth.fetch_request_token(self.request_token_url)
        return request_token_response.get("oauth_token")
    
    def check_auth(self):
        """ Raises error if user is not authenticated. """

        if not self.authenticated:
            raise UserNotAuthenticatedError()

    def _parse_accounts(self, response):
        """ Parses a list of Account objects from the XML response text. """

        accounts_dict = xmltodict.parse(response)
        accounts_list = accounts_dict["AccountListResponse"]["Accounts"]["Account"]
        accounts = [Account(**account, accountUser=self) for account in accounts_list]
        return accounts
        


    






        
