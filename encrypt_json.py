from cryptography.fernet import Fernet
import json
import base64

def encrypt_json_file(input_file, output_file, secret_key=None):
    # Use provided key or generate one if none provided
    if not secret_key:
        # Generate a key - only do this once and save it!
        key = Fernet.generate_key()
        print(f"Generated new key: {key.decode()}")
    else:
        # Convert string key to bytes if needed
        key = secret_key.encode() if isinstance(secret_key, str) else secret_key
    
    # Create a Fernet instance
    fernet = Fernet(key)
    
    # Read the JSON file
    with open(input_file, 'r') as file:
        json_data = json.load(file)
    
    # Convert JSON to string and encode to bytes
    json_string = json.dumps(json_data)
    json_bytes = json_string.encode()
    
    # Encrypt the data
    encrypted_data = fernet.encrypt(json_bytes)
    
    # Convert to base64 for easier transmission
    encrypted_base64 = base64.b64encode(encrypted_data).decode()
    
    # Save encrypted data
    with open(output_file, 'w') as file:
        file.write(encrypted_base64)

if __name__ == "__main__":
    # Use a static key (this should match what's in your React Native app)
    STATIC_KEY = "YOUR_STATIC_KEY_HERE"  # Must be 32 url-safe base64-encoded bytes
    encrypt_json_file('final_schema.json', 'encrypted_data.txt', STATIC_KEY)
