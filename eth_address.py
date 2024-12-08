from eth_account import Account

# Generate Ethereum address from private key
private_key = "your_private_key_here"
account = Account.from_key(private_key)
print("Ethereum Address:", account.address)

# Generate Ethereum address from seed phrase
seed_phrase = "your_seed_phrase_here"
account_from_seed = Account.from_mnemonic(seed_phrase)
print("Ethereum Address from Seed Phrase:", account_from_seed.address)
