def Dec_Bin(numero : int) -> str:
    cociente = 0
    residuo = 0
    bin = ""
    while numero / 2 > 0:
        cociente = int(numero) / 2
        residuo = int (numero) % 2
        numero = cociente
        bin = str(residuo) + bin

    bin = str(residuo) + bin
    return bin

def Bin_Dec (numero : str) -> int:
    decimal = 0
    i = 0
    j = len(numero) -1
    while j > 0:
        if numero[j] == "1":
            decimal += pow(2,i)
        i += 1
        j -= 1
    return decimal
def Dec_Oct (numero : int) -> str:
    octal = ""
    while numero > 0:
        octal = str(numero % 8) + octal
        numero = int(numero / 8)
    return octal

def Oct_Dec (numero : str) -> int:
    decimal = 0
    i = 0
    j = len(numero) -1
    while j > 0:
        decimal += int(numero[j]) * pow(8,i)
        i += 1
        j -= 1
    return decimal

def Dec_Hex (numero : int) -> str:
    hexa = ""
    while numero > 0:
        residuo = numero % 16
        if residuo < 10:
            hexa = str(residuo) + hexa
        else:
            hexa = chr(residuo + 55) + hexa
        numero = int(numero / 16)
    return hexa

def Hex_Dec (numero : str) -> int:
    decimal = 0
    i = 0
    j = len(numero) -1
    while j > 0:
        if numero[j].isalpha():
            decimal += (ord(numero[j]) - 55) * pow(16,i)
        else:
            decimal += int(numero[j]) * pow(16,i)
        i += 1
        j -= 1
    return decimal