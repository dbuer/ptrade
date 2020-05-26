import os
import ptrade
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    consumer_key = os.environ.get("sb_consumer_key")
    consumer_secret = os.environ.get("sb_consumer_secret")

    with ptrade.User(consumer_key, consumer_secret) as etrade_user:
        print("\nGet one account:")
        accountList = etrade_user.get_all_accounts()
        account = accountList[0]
        pprint(vars(account))

        print("\nGet account balances:")
        pprint(account.get_balances())

        print("\nQuote for Google:")
        pprint(etrade_user.get_quote(["GOOG"], ptrade.Detail.FUNDAMENTAL))

        print("\nOption expiries for Google")
        pprint(etrade_user.get_option_expires("GOOG"))
        
        print("\nOptions for Google:")
        pprint(etrade_user.get_option_chains("GOOG", "05"))



    
