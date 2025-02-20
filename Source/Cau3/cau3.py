import ast
from collections import Counter

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

    # Write cipherText to outputFile
    with open(outputFile, 'wb') as f:
        f.write(cipherText.encode())

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def is_python_source(byte_data):
    try:
        # Chuyển dãy byte thành chuỗi (giả định mã nguồn là dạng mã hóa UTF-8)
        source_code = byte_data
        # Cố gắng phân tích cú pháp (parse) mã nguồn thành cây cú pháp Python
        ast.parse(source_code)
        # Nếu thành công, trả về True (đây là mã nguồn Python hợp lệ)
        return True
    except (UnicodeDecodeError, SyntaxError):
        # Nếu gặp lỗi trong quá trình giải mã hoặc phân tích cú pháp, trả về False
        return False
    
def decrypt_without_a_b(inputFile, left, right):
    with open(inputFile, 'rb') as f:
        cipherText = f.read().decode('utf-8')

    for i in range(1, left):
        a_inv =  mod_inverse(i, 29) # a_inv holds the inverse of a under modulo 29
        if a_inv is None:
            raise ValueError(f"The value of 'a' does not have an inverse under modulo 29.")
            continue
        else:
            for j in range(1, right):
                text = ""
                for cipher in cipherText:
                    if cipher in codeTable:
                        # Convert letter to its corresponding number (‘A’=0, ‘B’=1, ‘C’=2 ...)
                        num = codeTable.index(cipher)
                        # Apply the affine_transformation-1: (a_*(C-b)) % 29
                        letter = codeTable[(a_inv * (num - j)) % 29]
                    else:
                        letter = cipher
                    # Append the letter to the text
                    text += letter
                if is_python_source(text) == True:
                    return text
                else :
                    continue
    return None
           
    with open(inputFile, 'rb') as f:
        cipherText = f.read().decode('utf-8')

    # Tính tần suất ký tự trong cipherText
    counter = Counter(cipherText)
    most_common_char, most_common_count = counter.most_common(1)[0]

    # Giả định rằng ký tự xuất hiện nhiều nhất trong văn bản tiếng Anh là 'E'
    # Tính b dựa trên ký tự xuất hiện nhiều nhất
    expected_char = 'e'
    expected_num = codeTable.index(expected_char)  # Chỉ số của 'E' trong codeTable
    most_common_num = codeTable.index(most_common_char)  # Chỉ số ký tự xuất hiện nhiều nhất

    # Tính toán b từ ký tự xuất hiện nhiều nhất
    b = (most_common_num - expected_num) % 29

    for i in range(1, left):
        a_inv = mod_inverse(i, 29)  # Tính nghịch đảo của a
        if a_inv is None:
            continue
        
        # Chỉ thử b đã tính toán
        text = ""
        for cipher in cipherText:
            if cipher in codeTable:
                num = codeTable.index(cipher)
                letter = codeTable[(a_inv * (num - b)) % 29]
            else:
                letter = cipher
            text += letter

        # Kiểm tra xem văn bản có phải là mã nguồn Python hợp lệ hay không
        if is_python_source(text):
            return text
    return None

#Test

plainText = """
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None
"""

a = 2972
b = 4235
left = 5000
right = 5000
outputFile = "Test.sec"

affine_encrypt(plainText, a, b, outputFile)
print("Encrypt....DONE")

result = decrypt_without_a_b(outputFile, left, right)
print("Decrypted Text:", result)