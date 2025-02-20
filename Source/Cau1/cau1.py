import random
import sys
import tkinter as tk
from tkinter import filedialog
import hashlib
"""
    encrypts the plaintext 'text', using an affine transformation key (a, b)
    :param text: str type; plaintext as a string of letters
    :param a: int type; #integer satisfying gcd(a, 29) = 1
    :param b: int type; shift value
    :param outputFile: str type; a string of output file name
"""

codeTable = "abcdefghijklmnopqrstuvwxyz., "

def affine_encrypt(text, a, b, outputFile):
    cipherText = ""
    for letter in text:
        if letter in codeTable:
            # Convert letter to its corresponding number (‘A’=0, ‘B’=1, ‘C’=2 ...)
            num = codeTable.index(letter)
            # Apply the affine transformation: (a * num + b) % 29
            cipher = codeTable[(a * num + b) % 29]
        else:
            cipher = letter # Preserve character if not in codeTable
        # Append the encrypted letter to the cipher text
        cipherText += cipher

    # Generate random a content bytes
    random_prefix = ""
    for i in range(a):
        random_number = random.randint(0, 28)
        random_prefix += codeTable[random_number]

    # Generate random b content bytes
    random_suffix = ""
    for i in range(b):
        random_number = random.randint(0, 28)
        random_suffix += codeTable[random_number]

    # Combine random bytes with cipherText
    final_output = (random_prefix + cipherText + random_suffix).encode()
    # Write cipherText to outputFile
    with open(outputFile, 'wb') as f:
        f.write(final_output)
# --------------------------------------------------------------------------
"""
    decrypts the given cipher, assuming it was encrypted using an affine
transformation key (a, b)
    :param inputFile: str type; a string of input file name
    :param a: int type; #integer satisfying gcd(a, 29) = 1.
    :param b: int type; shift value
    :return: str type; the decrypted message (as a string of uppercase letters)
"""
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_decrypt(inputFile, a, b):
    with open(inputFile, 'rb') as f:
        content = f.read()

    # Extract the actual ciphertext by skipping the random bytes
    cipherText = content[a:-b].decode('utf-8', errors='ignore')

    a_inv =  mod_inverse(a, 29) # a_inv holds the inverse of a under modulo 29
    if a_inv is None:
        raise ValueError(f"The value of 'a' does not have an inverse under modulo 29.")
    text = ""
    for cipher in cipherText:
        if cipher in codeTable:
            # Convert letter to its corresponding number (‘A’=0, ‘B’=1, ‘C’=2 ...)
            num = codeTable.index(cipher)
            # Apply the affine_transformation-1: (a_*(C-b)) % 29
            letter = codeTable[(a_inv * (num - b)) % 29]
        else:
            letter = cipher
        # Append the letter to the text
        text += letter
    return text

def convert_to_ascii_numbers(input_string):
    ascii_numbers = []
    for char in input_string:
        ascii_numbers.append(str(ord(char)))  # Chuyển đổi ký tự thành mã ASCII và thêm vào danh sách
    return ''.join(ascii_numbers)  # Kết hợp các số thành một chuỗi

def calculate_a_b_fromThePassWord(passwd):
    passwd_int = int(passwd)
    a = passwd_int % 2048
    if(a % 29 == 0):
        a = a + 25
    b = passwd_int % 1024
    return a, b

def hash_password(password):
    # Sử dụng SHA-256 để băm mật khẩu
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def save_password_to_file(hashed_password, filename):
    with open(filename, 'w') as file:
        file.write(hashed_password)

def check_hash_in_file(hash_value, filename):
    try:
        # Mở tệp và đọc nội dung
        with open(filename, 'r') as file:
            # Đọc tất cả các dòng và loại bỏ ký tự xuống dòng
            hashed_passwords = file.read().splitlines()
        
        # Kiểm tra xem hash_value có trong danh sách không
        if hash_value in hashed_passwords:
            return True
        else:
            return False
    except FileNotFoundError:
        print(f"Tệp {filename} không tồn tại.")
        return False

if __name__:
    if sys.argv[1]== '-encrypt':
        #Encrypt
        plaintext = input("Nhập một đoạn văn bản cần mã hóa: ") 
        passwd_input = input("Nhập mật khẩu: ")
        passwd = convert_to_ascii_numbers(passwd_input) #convert the password to an integer number
        a, b = calculate_a_b_fromThePassWord(passwd) #calculate a and b from the password
        outputFile = "Affine.sec" #the file will be stored the encrypted text
        passwordHashFile = "Password.txt" #the file will be stored the hashed password
        hash_password = hash_password(passwd) #hash the password
        save_password_to_file(hash_password, passwordHashFile) #save the password was hashed
        affine_encrypt(plaintext, a, b, outputFile)
        print("Encrypt.......DONE")

    elif sys.argv[1] == '-decrypt':
         #Decrypt
            #Select the file to decrypt
            print("Select the cipher file to decrypt: ")
            # Create a new tkinter window
            window = tk.Tk()
            window.withdraw() # Hide the window

            # Prompt the user to choose a file
            file_path_Decrypt = filedialog.askopenfilename()

            # Get just the file name
            file_name_Decrypt = file_path_Decrypt.split('/')[-1]
            print(file_name_Decrypt)

            # Close the tkinter window
            window.destroy()

            if file_name_Decrypt == '':
                print('Not Found File Decrypt')
            else:
                passwd_input = input("Nhập mật khẩu: ")
                passwd = convert_to_ascii_numbers(passwd_input)
                passwordHashFile = "Password.txt"
                hash_password = hash_password(passwd) #calculate the hash value of password
                if(check_hash_in_file(hash_password, passwordHashFile) == True):
                    a, b = calculate_a_b_fromThePassWord(passwd)
                    decrypted_text = affine_decrypt(file_name_Decrypt, a, b)
                    print("Decrypted Text:", decrypted_text)
                    print("Decrypt.......DONE")
                else:
                    print("Wrong password!")