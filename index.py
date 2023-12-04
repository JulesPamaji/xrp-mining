import hashlib
import time
import requests
import json

# XRP peer node 
PEER_URL = "http://xrp1.peer.org:51234"

def get_ledger():
    """ Gets latest ledger details from peer """
    
    url = f"{PEER_URL}/v1/ledger/current"
    resp = requests.get(url)
    data = resp.json()
    return data

def get_tx_data():
    """ Generates transaction data with random amount """
    
    source_address = "rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh" 
    destination = "ra5nK24KXen9AHvsdFTKHSANinZseWnPcX"
    amount = round(random.uniform(1, 100), 6)
    
    tx_data = {
       "TransactionType": "Payment",
       "Account": source_address,
       "Amount": str(amount),
       "Destination": destination  
    }
    
    return json.dumps(tx_data)
    

def submit_tx(tx_json):
    """ Submits transaction to peer network """
    
    url = f"{PEER_URL}/v1/transaction"
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url, headers=headers, data=tx_json)  
    print(resp.text)
    
def validate_tx(tx_id, ledger):
    """ Checks if transaction was accepted """
    
    # Get latest ledger transactions 
    url = f"{PEER_URL}{ledger['result']['ledger']['transactions']}"
    txs = requests.get(url).json()
    
    # Check if hash in transactions 
    for tx in txs:
        if tx["hash"] == tx_id:
            print("Validated successfully!")
            return True
        
    print("Not validated yet")    
    return False
    
def mine_xrp():
    """ Simple XRP mining demo """  
    
    # Get latest ledger index 
    ledger = get_ledger()
    print(f"Current ledger: {ledger['result']['ledger']['ledger_index']}")
    
    # Construct transaction 
    tx_json = get_tx_data() 
    
    # Submit transaction 
    resp = submit_tx(tx_json)
    tx_id = json.loads(resp)["result"]["transaction"]["hash"]
    
    # Validate inclusion 
    while True:
        if validate_tx(tx_id, ledger):
            print(f"Mined transaction: {tx_id}")
            break
            
        # Wait to check again 
        time.sleep(5)
        
if __name__ == "__main__":
    mine_xrp()
