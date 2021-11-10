import random
import math
import decimal
import os

decimal.getcontext().prec = 10000


def gcd(a, b):
    if a == 0:
        return b, 0, 1

    g, x1, y1 = gcd(b % a, a)

    x = y1 - (b//a) * x1
    y = x1
    return g, x, y


def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)+1)):
        if n % i == 0:
            return False
    return True


def primeFactors(n):
    res = [1]
    while (n % 2 == 0):
        res.append(2)
        n = n/2

    for i in range(3, int(math.sqrt(n))+1):
        while (n % i == 0):
            res.append(i)
            n = n/i

    if (n > 2):
        res.append(int(n))
    return res


def isCoPrime(a, b):
    if(gcd(a, b) == 1):
        return True
    factorA = primeFactors(a)
    factorB = primeFactors(b)
    count = 0
    for i in range(len(factorA)):
        if factorA[i] in factorB:
            count += 1
    if count == 1:
        return True
    return False


def generatePrime(numSize=2):
    x = 0
    while(isPrime(x) != True):
        x = random.randint(10**(numSize-1), 10**(numSize)-1)
    return x


def calcE(phi, n):
    for e in range(3, int(phi), 2):
        if isPrime(e):
            if isCoPrime(phi, e) == True:
                return e


# numSize: do dai cua p va q can duoc tao
def keyGen(numSize):
    p = generatePrime(numSize)
    q = generatePrime(numSize)
    print("p: ", p)
    print("q: ", q)
    while(p == q):
        q = generatePrime(numSize)

    n = p*q
    print("n: ", n)
    phi = (p-1)*(q-1)
    print("phi: ", phi)
    e = calcE(phi, n)
    print("e: ", e)
    # print(gcd(phi,e))
    d = gcd(phi, e)[2]
    while(d < 0):
        d += phi
    print("d: ", d)
    publicKey = (e, n)
    privateKey = (d, n)
    #print('Public key:', publicKey)
    #print('Private key:', privateKey)
    publicFile = open("rsa_pub.txt", "w+")
    publicFile.write(str(publicKey[0])+"\n"+str(publicKey[1]))
    privateFile = open("rsa.txt", "w+")
    privateFile.write(str(privateKey[0])+"\n"+str(privateKey[1]))
    return (publicKey, privateKey)


def numLen(n):
    n_str = str(n)
    return len(n_str)


def formalCipher(cipher, n):
    maxLen = numLen(n)
    res = ""
    for i in range(len(cipher)):
        padding = maxLen - numLen(cipher[i])
        res += padding*"0" + str(cipher[i])
    return res


def encrypt(publicKey, message):
    # tao ciphertext bang cach ma hoa moi ki tu trong plaintext theo gia tri ascii c=(m^e)%n
    # do dai cua moi phan tu trong ciphertext = do dai cua n
    cipher = []
    for i in range(len(message)):
        cipher.append(decimal.Context().power(
            ord(message[i]), publicKey[0], publicKey[1]))
        #cipher.append((ord(message[i]) ** publicKey[0]) % publicKey[1])
    #print("CIPHER: ", cipher)
    res = formalCipher(cipher, publicKey[1])
    f = open("encrypted.txt", "w+")
    f.write(res)
    return res


def formalMessage(plain):
    temp = ""
    res = ""
    for i in range(len(plain)):
        if(plain[i] == " "):
            res += temp+" "
            temp = ""
        else:
            temp += plain[i]
    res += temp
    return res


def collectCipherArray(cipher, n):
    maxLen = numLen(n)
    temp = ""
    res = []
    for i in range(0, len(cipher), maxLen):
        for j in range(i, i+maxLen):
            temp += cipher[j]
        res.append(int(temp))
        temp = ""
    return res


def decrypt(privateKey, cipher):
    # tao phaintext bang cach giai ma tung gia tri ascii cua moi chu trong ciphertext m=(c^d)%n
    # do dai cua moi phan tu trong ciphertext = do dai cua n
    cipherArray = collectCipherArray(cipher, privateKey[1])
    #print("COLLECTED CIPHER:", cipherArray)
    plain = []
    for i in range(len(cipherArray)):
        x = decimal.Decimal(cipherArray[i])
        x = decimal.Context().power(x, privateKey[0], privateKey[1])
        plain.append(chr(x))
    #print("PLAIN: ", plain)
    res = formalMessage(plain)
    
    f = open("decrypted.txt", "w+")
    f.write(res)
    return res


def readKey(filename):
    f = open(filename, "r")
    temp = f.readlines()
    f.close()
    return int(temp[0]), int(temp[1])

def readTxt(filename):
    f = open(filename, "r")
    temp = f.read()
    f.close()
    return temp

if __name__ == '__main__':
    #print("--------------GENERATING KEY PAIR--------------")
    #keyGen(8)
    print("--------------COLLECTING KEY PAIR--------------")
    publicKey = readKey("rsa_pub.txt")
    privateKey = readKey("rsa.txt")
    print("PUBLIC KEY: ", publicKey)
    print("PRIVATE KEY: ", privateKey)
    
    print("--------------ENCRYPTING WITH PUBLIC KEY-------------- ")
    #message = "VERY HELLO WORLD"
    filename = input("Input filename to be encrypted: ")
    message = readTxt(filename)
    #print("MESSAGE: ", message)
    publicFile = input("Input filename of your public key: ")
    publicKey = readKey(publicFile)
    encryptedMessage = encrypt(publicKey, message)
    #print("ENCRYPTED MESSAGE: ", encryptedMessage)
    print("--------------DECRYPTING WITH PRIVATE KEY--------------")
    filename2 = input("Input filename to be decrypted: ")
    message2 = readTxt(filename2)
    #print("MESSAGE: ", message)
    privateFile = input("Input filename of your private key: ")
    privateKey = readKey(privateFile)
    print("Original message is:")
    print(decrypt(privateKey, encryptedMessage))
