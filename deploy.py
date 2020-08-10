#!/usr/bin/env python
import json
import os
import sys
from web3 import Web3



def main():
    rpc='http://127.0.0.1:8545'
    web3 = Web3(Web3.HTTPProvider(os.getenv('EVENTS_RPC')))
    private_key= os.getenv('EVENTS_TESTS_PRIVATE_KEY')
    path = './aquarius/artifacts/DDO.json'
    data=json.load(open(path))
    address=deploy_contract(web3,data,private_key)
    print(address)

def deploy_contract(w3, _json,private_key):
    account = w3.eth.account.privateKeyToAccount(private_key)
    _contract = w3.eth.contract(abi=_json['abi'], bytecode=_json['bytecode'])
    built_tx = _contract.constructor().buildTransaction({'from': account.address})
    if 'gas' not in built_tx:
        built_tx['gas'] = w3.eth.estimateGas(built_tx)
    raw_tx = sign_tx(w3,built_tx, private_key)
    tx_hash = w3.eth.sendRawTransaction(raw_tx)
    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    #return cls.get_tx_receipt(tx_hash, timeout=60).contractAddress
    return address

def sign_tx(web3, tx,private_key):
        account = web3.eth.account.privateKeyToAccount(private_key)
        nonce = web3.eth.getTransactionCount(account.address)
        gas_price = int(web3.eth.gasPrice / 100)
        tx['gasPrice'] = gas_price
        tx['nonce'] = nonce
        signed_tx = web3.eth.account.signTransaction(tx, private_key)
        return signed_tx.rawTransaction  
    

def setenv(key, value):
    # os.putenv(key, value) #Do *not* use putenv(), it doesn't work
    os.environ[key] = value


if __name__ == '__main__':
    main()