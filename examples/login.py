import ptrade

import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    consumer_key = os.environ.get("sb_consumer_key")
    consumer_secret = os.environ.get("sb_consumer_secret")
    try:
        etrade_user = ptrade.User(consumer_key, consumer_secret)
        token = etrade_user.login()
        print(token)
    except Exception as e:
        print(e)
    finally:
        etrade_user.logout()


    
