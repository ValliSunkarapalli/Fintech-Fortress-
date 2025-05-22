# common/common.py
import socket

def __encrypt(unencryptedData: str, key: int) -> bytes:
    asc = [ord(char) for char in unencryptedData]
    return bytes([char ^ key for char in asc])

def __decrypt(encryptedData: bytes, key: int) -> str:
    decryptedData = bytes([byte ^ key for byte in encryptedData])
    return decryptedData.decode("utf-8")

def sendEncryptedMessage(sock: socket.socket, message: str, key: int) -> list:
    try:
        encryptedMessage = __encrypt(message, key)
        sock.send(encryptedMessage)
        return [True]
    except Exception as e:
        return [False, e]

def recvEncryptedMessage(sock: socket.socket, key: int) -> list:
    try:
        data = sock.recv(1024)
        if not data:
            return [False, "No data received"]
        message = __decrypt(data, key)
        return [True, message]
    except Exception as e:
        return [False, e]
