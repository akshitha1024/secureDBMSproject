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