print ("Health Care Profession")
#Import Packages for Deploying the Smart Contract
import time
import json
import web3
from eth_account import Account
from web3.auto import w3
from web3.providers.websocket import WebsocketProvider
from web3 import Web3
from solc import compile_standard


#Get the HealthCare Smart Contract
with open("HealthCare.sol") as contract:
 contractText=contract.read()

#Get the Private Key for deploying the contract
with open(".pk") as pkfile:
 privateKey=pkfile.read()

#Get Infura ID fo deploying on an Ethereum Testnet(Rinkeby)
with open(".infura") as infurafile:
 infuraKey=infurafile.read()



# Solidity source code
compiled_sol = compile_standard({
     "language": "Solidity",
     "sources": {
         "HealthCare.sol": {
             "content": contractText
         }
     },
     "settings":
         {
             "outputSelection": {
                 "*": {
                     "*": [
                         "metadata", "evm.bytecode"
                         , "evm.bytecode.sourceMap"
                     ]
                 }
             }
         }
})
bytecode = compiled_sol['contracts']['HealthCare.sol']['HealthCare']['evm']['bytecode']['object']
abi = json.loads(compiled_sol['contracts']['HealthCare.sol']['HealthCare']['metadata'])['output']['abi']
W3 = Web3(WebsocketProvider('wss://rinkeby.infura.io/ws/v3/%s'%infuraKey))
_account=Account.from_key(privateKey);
_address=_account.address
HealthCare = W3.eth.contract(abi=abi, bytecode=bytecode)
nonce = W3.eth.getTransactionCount(_address)
print(nonce)

# Submit the transaction that deploys the contract
build_txn = HealthCare.constructor().buildTransaction({
'chainId': 4,
'gas': 1400000,
'gasPrice': w3.toWei('40', 'gwei'),
'nonce': nonce,
'from':_address
})
signed_txn = W3.eth.account.sign_transaction(build_txn, private_key=privateKey)
print(signed_txn)

#Deploy smart contract 
print("Deploying the HealthCare Smart Contract")
result = W3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(result)
print('##################################')
txn_receipt = W3.eth.getTransactionReceipt(result)

count = 0
while tx_receipt is None and (count < 200):
  time.sleep(1)
  try:
    tx_receipt = W3.eth.getTransactionReceipt(result)
  except:
    print('#')

if txn_receipt is None:
  print (" {'status': 'failed', 'error': 'timeout'} ")
print (txn_receipt)
print("Health Care Smart Contract address is:",txn_receipt.contractAddress)
#Health Care Smart Contract address is: 0xc943FA5233988B348b70458c23bcDe656d2478d0

health_care = W3.eth.contract(
  address=tx_receipt.contractAddress,
  abi=abi
)
print(health_care.functions.profession().call())
nonce = W3.eth.getTransactionCount(_address)
build_txn = health_care.functions.setProfession('I am a Medical Doctor by Profession with an ID - 10556535').buildTransaction({
  'chainId': 4,
  'gas': 1400000,
  'gasPrice': w3.toWei('40', 'gwei'),
  'nonce': nonce,
  'from':_address
})

signed_txn = W3.eth.account.sign_transaction(build_txn, private_key=privateKey)
result = W3.eth.sendRawTransaction(signed_txn.rawTransaction)
txn_receipt = W3.eth.getTransactionReceipt(result)

count = 0
while txn_receipt is None and (count < 200):
  time.sleep(1)
  try:
    txn_receipt = W3.eth.getTransactionReceipt(result)
  except:
    print('.')

if txn_receipt is None:
  print (" {'status': 'failed', 'error': 'timeout'} ")

txn_hash = health_care.functions.setProfession('I am a Nurse by Profession with an ID - 10556535 ').transact({"from":_account.address})
txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
print("Result from myProfession()")
print(health_care.functions.myProfession().call({"from":_account.address}))
