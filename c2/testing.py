from PIL import Image

def stringToBinary(string):

    stringLength = len(string)
    if stringLength == 0:
        return ""

    intString = []
    for c in range(stringLength):#converts string into integer form (ASCII)
        intString.append(ord(string[c]))
    
    binString = []
    for i in range(stringLength):#into an array of string formed bits
        binString.append(bin(intString[i]))
        binString[i] = binString[i][2:]#string

        if (len(binString[i]) < 7):#pad the zeros into ASCII binary form 
            for k in range(len(binString[i]),7):                    
                binString[i] = "0" + binString[i]
            
    print("join")
    returnString = "".join(binString)
    returnString = returnString + "0000000" #add the null byte
    return returnString


def main():

    img = Image.open("joe.jpg")
    img_rgb = img.convert("RGB")
    (width, height) = img.size
    pix = img.load()
    print("0 0 before")
    print(pix[0,0])
    
    print(img)
    new_img = img.copy()
    pix3 = img.load()
    #new_img = new_img.convert("RGB")
    pix = new_img.load()
    print(pix[0,0])
    print(pix3[0,0])

    # for i in range(height):
    #     for j in range(width):
    #         (r,g,b) = pix[j,i]
    #         pix[j,i] = (r,g,b)

    # print("0 0 after")
    # print(pix[0,0])

    img_name = "btest.jpg"
    new_img.save(('/Users/justinwong/Documents/GitHub/c2-server/c2/' + img_name))

if __name__ == "__main__":
    main()