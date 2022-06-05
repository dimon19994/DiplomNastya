from web3 import Web3, HTTPProvider

from config import NODE_URL
from models import Wallet
from utils import get_base_58_string, convert_from_wei, convert_to_wei


class EthProtocol:
    def __init__(self):
        self.client = Web3(HTTPProvider(NODE_URL))
        self.abi = [
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "_from",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "address",
          "name": "_to",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "_amount",
          "type": "uint256"
        }
      ],
      "name": "Transaction",
      "type": "event"
    },
    {
      "constant": True,
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "balances",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": False,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": False,
      "inputs": [
        {
          "internalType": "address",
          "name": "_address",
          "type": "address"
        }
      ],
      "name": "createBalance",
      "outputs": [],
      "payable": False,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": True,
      "inputs": [
        {
          "internalType": "address",
          "name": "_address",
          "type": "address"
        }
      ],
      "name": "getBalance",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "balance",
          "type": "uint256"
        }
      ],
      "payable": False,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": False,
      "inputs": [
        {
          "internalType": "address",
          "name": "_from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "_to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_amount",
          "type": "uint256"
        }
      ],
      "name": "transaction",
      "outputs": [
        {
          "internalType": "string",
          "name": "message",
          "type": "string"
        },
        {
          "internalType": "bool",
          "name": "result",
          "type": "bool"
        }
      ],
      "payable": False,
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]
        self.contract_address = "0xafcC066A7A5ac6219e31D64f0B3AF0563dcE319E"

    def create_wallet(self, password=None):
        if password is None:
            password = get_base_58_string(30)

        address = get_base_58_string(30)

        #contract = self._get_contract()
        #contract.functions.createBalance(Web3.toChecksumAddress(address)).call()

        wallet = Wallet.create(address=address,
                               password=password, balance=0)
        return wallet

    def get_balance(self, address):
        contract = self._get_contract()

        address = Web3.toChecksumAddress(address)

        balance = convert_from_wei(contract.functions.getBalance(address).call())

        return balance

    def transaction(self, from_address, to_address, amount):
        _from = Web3.toChecksumAddress(from_address)
        _to = Web3.toChecksumAddress(to_address)
        _amount = convert_to_wei(amount)

        contract = self._get_contract()

        message, result = contract.functions.transaction(_from, _to, _amount).call()

        print(message, result)

    def _get_contract(self):
        return self.client.eth.contract(address=Web3.toChecksumAddress(self.contract_address), abi=self.abi)
