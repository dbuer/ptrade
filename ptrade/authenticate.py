import logging
import enum
import webbrowser

from requests_oauthlib import OAuth1Session
from oauthlib.common import add_params_to_uri

ETRADE_LOGIN_URL = "https://us.etrade.com/e/t/etws/authorize"
OAUTH_BASE_URL = "https://api{}.etrade.com/oauth/"

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
        self.request_token_url = self.oauth_base_url + "request_token"
        self.access_token_url = self.oauth_base_url + "access_token"
        self.renew_token_url = self.oauth_base_url + "renew_access_token"
        self.revoke_token_url = self.oauth_base_url + "revoke_access_token"
        
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
        
        self._check_auth()
        response = self.oauth.get(self.revoke_token_url)
        self.oauth = None
        response.raise_for_status()
        return True

    def renew(self):
        """ Renews the user access token. Access token becomes inactive 
            if your application does not make API requests for two hours. """
        
        self._check_auth()
        response = self.oauth.get(self.renew_token_url)
        response.raise_for_status()
        return True

    def _get_request_token(self):
        """ Request tokens are valid for 5 minutes. """

        request_token_response = self.oauth.fetch_request_token(self.request_token_url)
        return request_token_response.get("oauth_token")
    
    def _check_auth(self):
        """ Raises error if user is not authenticated. """

        if not self.authenticated:
            raise UserNotAuthenticatedError()

    






        
