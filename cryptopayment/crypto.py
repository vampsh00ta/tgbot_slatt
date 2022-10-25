from web3 import Web3,HTTPProvider
import requests
from random import  randrange
import time
class EthModule(object):
    ETHER_VALUE = 10 ** 18
    COIN_GECKO_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd'
    def __init__(self,httpprovider,api_key,base_url,wallet,waiting_time):
        self.web3 = Web3(HTTPProvider(httpprovider))
        self.API_KEY = api_key
        self.BASE_URL = base_url
        self.wallet = wallet
        self.waiting_time = int(waiting_time)

    def make_api_url(self,module, action, **kwargs):
        url = self.BASE_URL + f"?module={module}&action={action}&apikey={self.API_KEY}"

        for key, value in kwargs.items():
            url += f"&{key}={value}"
        return url

    def checkDeposit(self,deposit):
        block = self.web3.eth.get_block('latest')
        transactions_url = self.make_api_url(module="account", action="txlist", address=self.wallet,
                                             startblock=block['number'],
                                             endblock=99999999, page=1, offset=10,
                                             sort="asc")

        start = time.time()
        while True:
            response =  requests.get(transactions_url)
            data = response.json()["result"]
            for tx in data:
                if tx['to'].lower() == self.wallet.lower() and float(tx['value'])/self.ETHER_VALUE == deposit:
                    return True
            end = time.time()
            if end - start >= self.waiting_time*60:
                return False


    def convertFiat(self,amount):
        eth_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=rub')
        eth_amount =float(amount/eth_response.json()['ethereum']['rub'])
        eth_amount = f"{eth_amount:.8f}"
        result = list(eth_amount)
        result[8] = str(randrange(0, 9))
        result[9] = str(randrange(0, 9))
        result = ''.join(result)
        deposit = float(result)
        return deposit


