import requests

def get_transaction_details(address, api_key):
    """
    Fetch transaction details for a given Bitcoin address using BlockCypher API.
    """
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/full?token={api_key}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching data. HTTP Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            return None
        return response.json()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def recover_public_key_from_transaction(address, api_key):
    """
    Recover the public key from a Bitcoin address if the address has sent Bitcoin (i.e., has inputs).
    """
    # Fetch the transaction data for the address
    data = get_transaction_details(address, api_key)
    
    if not data or 'txs' not in data:
        print(f"No transaction data found for address {address}.")
        return None
    
    transactions = data['txs']
    
    if not transactions:
        print("No transactions found for this address.")
        return None
    
    # Iterate over transactions to find public key from the scriptSig or witness
    for tx in transactions:
        tx_hash = tx['hash']
        print(f"Checking transaction: {tx_hash}")
        
        # Check inputs to see if the public key is included
        for input_tx in tx['inputs']:
            # In P2PKH transactions, the scriptSig includes the public key
            if 'script' in input_tx:
                script = input_tx['script']
                
                # A typical P2PKH scriptSig contains the public key (in the signature and public key)
                if len(script) >= 106:  # Minimum length for P2PKH scriptSig
                    # Extract the public key from the script (simplified)
                    # Public key is at the end of the scriptSig (assuming the script is in the standard format)
                    pub_key_start = script[64:104]  # This is simplified, might need to adjust
                    print(f"Public key found: {pub_key_start}")
                    return pub_key_start
    
    print("No public key found in transactions.")
    return None
import requests

def get_transaction_details(address, api_key):
    """
    Fetch transaction details for a given Bitcoin address using BlockCypher API.
    """
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/full?token={api_key}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching data. HTTP Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            return None
        return response.json()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def recover_public_key_from_transaction(address, api_key):
    """
    Recover the public key from a Bitcoin address if the address has sent Bitcoin (i.e., has inputs).
    """
    # Fetch the transaction data for the address
    data = get_transaction_details(address, api_key)
    
    if not data or 'txs' not in data:
        print(f"No transaction data found for address {address}.")
        return None
    
    transactions = data['txs']
    
    if not transactions:
        print("No transactions found for this address.")
        return None
    
    # Iterate over transactions to find public key from the scriptSig or witness
    for tx in transactions:
        tx_hash = tx['hash']
        print(f"Checking transaction: {tx_hash}")
        
        # Check inputs to see if the public key is included
        for input_tx in tx['inputs']:
            # In P2PKH transactions, the scriptSig includes the public key
            if 'script' in input_tx:
                script = input_tx['script']
                
                # For P2PKH, the scriptSig contains the public key after the signature
                if len(script) >= 106:  # Minimum length for P2PKH scriptSig
                    # Extract the public key (compressed or uncompressed)
                    # Compressed public key: 33 bytes (0x02 or 0x03 prefix)
                    # Uncompressed public key: 65 bytes (0x04 prefix)
                    pub_key_start = script[64:104]  # Extracting the public key part (simplified)
                    print(f"Public key found: {pub_key_start}")
                    return pub_key_start
                
            # Check witness for SegWit transactions (P2WPKH, P2WSH)
            if 'witness' in input_tx:
                for witness_item in input_tx['witness']:
                    # Witness for P2WPKH should be a compressed public key
                    if len(witness_item) == 66:  # Compressed public key length
                        print(f"Public key from SegWit found: {witness_item}")
                        return witness_item
    
    print("No public key found in transactions.")
    return None

# Example usage
if __name__ == "__main__":
    address = '1MqWUyivo9sj323sirtbxZ1S23vPA36FDK'
    api_key = '047e28d015d64bb9b6de2708e1117eec'
    public_key = recover_public_key_from_transaction(address, api_key)
    if public_key:
        print(f"Recovered Public Key: {public_key}")
    else:
        print("Could not recover public key.")

