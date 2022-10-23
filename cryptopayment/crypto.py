from web3 import Web3, HTTPProvider
import asyncio
import asyncio
import json
import requests
from web3 import Web3
from websockets import connect
import threading
import time
account = '0xce479Ff6fDdC5E162861375E0A230357c101F22e'
subscriptions = {
    # Example of dict structure
    'chat_id': {
        'wallet_addr': [] # List of most recent transactions
    }
}
def background(f):
    def backgrnd_func(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return backgrnd_func

def transactions(wallet: str = None) -> list:
    assert (wallet is not None)
    url_params = {
        'module': 'account',
        'action': 'txlist',
        'address': wallet,
        'startblock': 0,
        'endblock': 99999999,
        'page': 1,
        'offset': 10,
        'sort': 'asc',
        'apikey': 'RHCTJPJ811MD3QYBCQ134WBXQT6DSA7CXW'
    }

    response = requests.get('https://api.etherscan.io/api', params=url_params)
    response_parsed = json.loads(response.content)
    assert (response_parsed['message'] == 'OK')
    txs = response_parsed['result']
    return [{'from': tx['from'], 'to': tx['to'], 'value': tx['value'], 'timestamp': tx['timeStamp']} \
            for tx in txs]


def update_subscriptions(chat_id, wallet) -> bool:
    global subscriptions
    try:
        txs = transactions(wallet)
        if chat_id not in subscriptions.keys():
            subscriptions[chat_id] = {}
        subscriptions[chat_id][wallet] = txs
        return True
    except:
        return False
def get_latest_tx(txs: list) -> int:
    return max(txs,key=lambda tx: int(tx['timestamp']))
def format_tx(tx: dict) -> str:
    return f'From: {tx["from"]}, To: {tx["to"]}, Amount: {tx["value"]}'

