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
    #test = 50000000
    #test2 = test.to_bytes(6,"little")


    # width = 200
    # height = 200
    # command = "hello xd"
    # num_pixels = width * height
    # offset = random.randint(2, num_pixels)#endpoints are included
    # offsetpos = ((int)(offset/width), (offset%width)) #pixel position for offset
    # offset_byte = offset.to_bytes(6,"little")
    # print(offset_byte)

    # print("offset number: {}".format(offset))
    # print("offset byte: {}".format(offset_byte))
    # print(offset_byte.decode('UTF-8'))

    # binary = bin(2)
    # binary = binary[2:]
    # print("binary: " + binary)

    # for j in range(1,7):
    #     print(j)

    # if (len(binary) < 6):#pad the zeros
    #         for i in range(len(binary),8):
    #             binary = "0"+ binary

    # print(binary)

    # iid = 102
    # img_name = "{}_diniFall.jpg".format(iid)
    # print("img_name: " + img_name)

    # tester = "I am a test string!"
    # print(tester.encode('ascii'))

    # print(ord('a'))
    # arr = []

    # print(stringToBinary("hi"))
    # print(stringToBinary(""))

    # arr.append("SHEESH")
    # arr.append("ya yeet")
    # print(arr)

    # img = Image.open("joe.jpg")
    # img_rgb = img.convert("RGB")
    # (width, height) = img.size

    img = Image.open("joe.jpg")
    img_rgb = img.convert("RGB")
    (width, height) = img.size
    pix = img.load()
    print("0 0 before")
    print(pix[0,0])

    new_img = img.copy()
    new_img = new_img.convert("RGB")
    pix = new_img.load() 

    for i in range(height):
        for j in range(width):
            (r,g,b) = pix[j,i]
            pix[j,i] = (r,g,1)

    print("0 0 after")
    print(pix[0,0])

    img_name = "btest.jpg"
    new_img.save(('/Users/justinwong/Documents/GitHub/c2-server/c2/' + img_name), format="JPEG")

if __name__ == "__main__":
    main()