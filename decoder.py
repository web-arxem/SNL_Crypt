from Crypto.Cipher import AES
import base64

# Функция для расшифрования текста
def decrypt_text(key, ciphertext):
    data = base64.b64decode(ciphertext.encode())
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_text.decode()  # вернем расшифрованный текст в виде строки

# Введите зашифрованный текст для дешифровки
encrypted_text = input("Введите зашифрованный текст для дешифровки: ")
# Введите ключ шифрования
key = input("Введите ключ шифрования для дешифровки (введите ключ в base64): ")
key = base64.b64decode(key)

# Расшифровываем текст и выводим результат
decrypted_text = decrypt_text(key, encrypted_text)
print("Расшифрованный текст:", decrypted_text)

# Добавляем ожидание нажатия клавиши Enter перед завершением программы
input("Нажмите Enter для завершения программы...")