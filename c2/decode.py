import random
from bitstring import BitArray


def stringToBinary(string):
    stringLength = len(string)
    intString = []

    if stringLength == 0:
        return ""

    for c in range(stringLength):#converts string into integer form (ASCII)
        intString.append(ord(string[c]))
    
    binString = []
    for i in range(stringLength):#into an array of string formed bits
        binString.append(bin(intString[i]))
        binString[i] = binString[i][2:] #string

        if (len(binString[i]) < 7):#pad the zeros into ASCII binary form 
            for i in range(len(binString[i]),7):                    
                binString[i] = "0" + binString[i] #"0{}".format(binString[i])
                print("test")

    returnString = "".join(binString)
    returnString = returnString + "0000000"
    return returnString




def main():
    


if __name__ == "__main__":
    main()