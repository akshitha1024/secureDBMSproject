import bcrypt
import mysql.connector

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Varshini4260",
        database="SecureHealthcareDB"
    )

# Register a user
def register_user(username, password, group_type):
    conn = connect_db()
    cursor = conn.cursor()
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO Users (username, password_hash, group_type) VALUES (%s, %s, %s)",
                       (username, password_hash, group_type))
        conn.commit()
        print(f"User {username} registered successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Authenticate a user
def authenticate_user(username, password):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
        print(f"User {username} authenticated successfully.")
        return user['group_type']
    else:
        print("Authentication failed.")
        return None

# Example usage
#register_user("akshitha", "password", "H")
#user_group = authenticate_user("akshitha", "password")

def query_data(group_type):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    if group_type == "H":
        cursor.execute("SELECT * FROM HealthcareInfo")
    elif group_type == "R":
        cursor.execute("SELECT gender, age, weight, height, health_history FROM HealthcareInfo")
    else:
        print("Invalid group type.")
        return
    
    results = cursor.fetchall()
    for row in results:
        print(row)
    
    cursor.close()
    conn.close()

# Example usage
#user_group = authenticate_user("akshitha", "password")
#query_data(user_group)

import hashlib

def verify_data_integrity(data):
    hash_value = hashlib.sha256(str(data).encode()).hexdigest()
    return hash_value

# Example usage
#data = {"gender": 0, "age": 30, "weight": 60.0, "height": 165.5, "health_history": "No issues."}
#checksum = verify_data_integrity(data)
#print(f"Data checksum: {checksum}")

def verify_query_completeness(results):
    concatenated_data = "".join(str(row) for row in results)
    hash_value = hashlib.sha256(concatenated_data.encode()).hexdigest()
    return hash_value

# Example usage
#query_result = [{"gender": 0, "age": 30, "weight": 60.0, "height": 165.5, "health_history": "No issues."}]
#completeness_hash = verify_query_completeness(query_result)

from cryptography.fernet import Fernet

# Generate a key (do this once and store securely)
# key = Fernet.generate_key()
# Save the key securely (e.g., environment variable)
key = Fernet.generate_key()

# Print the key (you must save this securely for future use)
print(f"Generated Key: {key.decode()}")

# Example of using the generated key
#Generated Key: oQZJgHBoQRwtq9Obz8HSDt2S-kmoMWOvy7I7z-wbNz4=
#Encrypted Gender: b'gAAAAABnTQxVVdfQcEUocSScfWaw2dyAkx7EsqeluqS7DyF3WvXiZZ3Z-KBS6jC6TOf2_f5Xxrwedz-ta8l7AiOuBlT0GvlK2Q=='       
#Decrypted Gender: 1
cipher = Fernet(key)

def encrypt_data(data):
    return cipher.encrypt(data.encode())

def decrypt_data(encrypted_data):
    return cipher.decrypt(encrypted_data).decode()

# Example usage
#encrypted_gender = encrypt_data("1")  # Encrypt gender (as string)
#print(f"Encrypted Gender: {encrypted_gender}")

#decrypted_gender = decrypt_data(encrypted_gender)
#print(f"Decrypted Gender: {decrypted_gender}")

#extra points

import random

# Define a custom OPE encryption scheme
class SimpleOPE:
    def __init__(self, key):
        random.seed(key)  # Use a fixed key for deterministic behavior
        self.offset = random.randint(100, 1000)  # Random offset for encryption

    def encrypt(self, plaintext):
        return plaintext + self.offset  # Add offset to plaintext

    def decrypt(self, ciphertext):
        return ciphertext - self.offset  # Subtract offset from ciphertext

# Example usage of the custom OPE
ope_key = "secure_key"
ope_cipher = SimpleOPE(ope_key)

# Encrypt and decrypt an example weight
plaintext_weight = 72.5
encrypted_weight = ope_cipher.encrypt(plaintext_weight)
decrypted_weight = ope_cipher.decrypt(encrypted_weight)

print(f"Plaintext: {plaintext_weight}, Encrypted: {encrypted_weight}, Decrypted: {decrypted_weight}")

import mysql.connector

def update_weights_with_custom_ope():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Fetch all weights
    cursor.execute("SELECT id, weight FROM HealthcareInfo")
    rows = cursor.fetchall()

    # Encrypt weights
    for row in rows:
        encrypted_weight = ope_cipher.encrypt(row['weight'])
        cursor.execute("UPDATE HealthcareInfo SET weight = %s WHERE id = %s", (encrypted_weight, row['id']))

    conn.commit()
    cursor.close()
    conn.close()
    print("Weights updated with custom OPE encryption.")

update_weights_with_custom_ope()

def range_query_custom_ope(min_weight, max_weight):
    encrypted_min = ope_cipher.encrypt(min_weight)
    encrypted_max = ope_cipher.encrypt(max_weight)

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Perform the range query
    cursor.execute(
        "SELECT id, weight FROM HealthcareInfo WHERE weight BETWEEN %s AND %s",
        (encrypted_min, encrypted_max)
    )
    results = cursor.fetchall()

    # Decrypt the weights for display
    for row in results:
        row['weight'] = ope_cipher.decrypt(row['weight'])
        print(row)

    cursor.close()
    conn.close()

# Example usage
range_query_custom_ope(60.0, 80.0)


