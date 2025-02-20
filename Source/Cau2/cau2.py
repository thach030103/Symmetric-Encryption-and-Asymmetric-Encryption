import random
from math import gcd
"""
Generate the RSA key
:param p: int type; prime number used as part of the key n = p * q to encrypt the ciphertext
:param q: int type; prime number used as part of the key n = p * q to encrypt the ciphertext
:return: tuple type; publicKey=(n,e) and privateKey=(n,d)
"""
def mod_inverse(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    return None

def generate_rsa_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.choice([x for x in range(2, phi) if gcd(x, phi) == 1])
    d = mod_inverse(e, phi) # FIXME: Compute the inverse of e (mod phi)
    publicKey = (n, e)
    privateKey = (n, d)
    return publicKey, privateKey
"""
encrypts the plainText using RSA and the key (p*q, e)
:param plainText: str type; the orignal message as a string of letters
:param publicKey: tuple type; the key (n, e) to encrypt the plainText
:param outputFile: str type; a string of output file name
"""
def rsa_encrypt(plainText, publicKey, outputFile):
    n, e = publicKey
    plainTextBytes = [ord(char) for char in plainText] 
    cipherText = [pow(byte, e, n) for byte in plainTextBytes] 
    # FIXME # Write cipherText to outputFile
    with open(outputFile, 'w') as file:
        for encrypted_byte in cipherText:
            file.write(str(encrypted_byte) + "\n")
"""
decrypts the cipherText in the inputFile, which was encrypted using RSA and the key (p*q, e)
:param inputFile: str type; as a string of input file name
:param privateKey: tuple type; the key (n, d) to decrypt the ciphertext
:return: str type; the decrypted message as a string of letters
"""
def rsa_decrypt(inputFile, privateKey):
    n, d = privateKey
    # FIXME # Read cipherText from file
    with open(inputFile, 'r') as file:
        cipherText = [int(line.strip()) for line in file]

    decryptedBytes = [pow(char, d, n) for char in cipherText] 
    plainText = ''.join([chr(byte) for byte in decryptedBytes]) 
    return plainText

def main():

    # Generate RSA keys
    publicKey, privateKey = generate_rsa_keys(31847,28579)
    print("Public Key:", publicKey)
    print("Private Key:", privateKey)

    # Plain text to encrypt
    plainText = "Ma hoa RSA"

    # Encrypt the plainText and write to a file
    outputFile = "encrypted.txt"
    rsa_encrypt(plainText, publicKey, outputFile)

    # Read cipherText from a file and decrypt 
    decryptedText = rsa_decrypt(outputFile, privateKey)
    print("Decrypted message:", decryptedText)

if __name__ == "__main__":
    main()