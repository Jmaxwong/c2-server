from PIL import Image
import random

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
        binString[i] = binString[i][2:] #string

        if (len(binString[i]) < 7):#pad the zeros into ASCII binary form 
            for i in range(len(binString[i]),7):                    
                binString[i] = "0" + binString[i]
                print("test")

    returnString = "".join(binString)
    returnString = returnString + "0000000" #add the null byte
    return returnString

#NOTE**** IT IS (col,row) NOT (row,col)
def encodeImage(commands, img, iid):  # img is string of file ("diniFall.png") and commands is expected to be arr size 3
    try:
        img = Image.open(img)
        img_rgb = img.convert("RGB")
        (width, height) = img.size
        print("width: {}".format(width))
        print("height: {}".format(height))
        new_img = img.copy()
        #(r, g, b) = img_rgb.getpixel((0, 0))
    
    except:
        print("ERROR: No file found!")


    print("Checkpoint 1")
    def evenRGB(num, col, row): #num is an integer referring to r, g, or b
        (r,g,b) = img_rgb.getpixel((col,row)) 
        if num == 1:
            if(r%2 == 0):# THIS IS NOT NECESSARY BC ITS EVEN ONLY USEFUL IN ODD
                return 0
            else:
                if(r == 0):
                    new_img.putpixel((col,row), (r+1,g,b) )
                else:
                    new_img.putpixel((col,row), (r-1,g,b) )
        if num == 2:
            if(g%2 == 0):
                return 0
            else:
                if(r == 0):
                    new_img.putpixel((col,row), (r,g+1,b) )
                else:
                    new_img.putpixel((col,row), (r,g-1,b) )
        if num == 3:
            if(b%2 == 0):
                return 0
            else:
                if(r == 0):
                    new_img.putpixel((col,row), (r,g,b+1) )
                else:
                    new_img.putpixel((col,row), (r,g,b-1) )

    def oddRGB(num, col, row):
        (r,g,b) = img_rgb.getpixel((col,row))
        if num == 1:
            if(r%2 == 1):
                return 0
            else:
                if(r == 0):
                    new_img.putpixel((col,row), (r+1,g,b) )
                else:
                    new_img.putpixel((col,row), (r-1,g,b) )
        if num == 2:
            if(g%2 == 1):
                return 0
            else:
                if(r == 0):
                    new_img.putpixel((col,row), (r,g+1,b) )
                else:
                    new_img.putpixel((col,row), (r,g-1,b) )
        if num == 3:
            if(b%2 == 1):
                return 0
            else:
                if(r == 0):
                    new_img.putpixel((col,row), (r,g,b+1) )
                else:
                    new_img.putpixel((col,row), (r,g,b-1) )


    num_commands = 0
    if(commands[0] == ""):
        return 0
    elif(commands[1] == ""):
        oddRGB(1,0,0)
        evenRGB(2,0,0)
        evenRGB(3,0,0)
        num_commands = 1
    elif(commands[2] == ""):
        oddRGB(1,0,0)
        oddRGB(2,0,0)
        evenRGB(3,0,0)
        num_commands = 2        
    else:
        oddRGB(1,0,0)
        oddRGB(2,0,0)
        oddRGB(3,0,0)
        num_commands = 3 
            

    
    #TODO: make sure offset does not exceed the image size

    offset = random.randint(3, 63)

    #checks if offset is invalid
    print("Checkpoint 2")
    while (offset > (width*height)):
        print("ERROR: INVALID OFFSET GENERATED")
        print("Offset: " + offset)
        offset = random.randint(3, 63)     
    
    #position of offset coordinate
    (x, y) = ((offset % width), (int)(offset/width))

    #2nd and third pixel rgb conversion
    print("Checkpoint 3")
    binary_offset = (bin(offset))[2:]
    binary_offset_size = len(binary_offset)
    if (binary_offset_size < 6):#pad the front with zeros
        for count in range(binary_offset_size,6):
            binary_offset = "0"+ binary_offset

    for i in range(6):
        rgb = i%3 + 1
        if i <= 3:
            if binary_offset[i] == "1":
                oddRGB(rgb,1,0)
            else:
                evenRGB(rgb,1,0)
        else:
            if binary_offset[i] == "1":
                oddRGB(rgb,2,0)
            else:
                evenRGB(rgb,2,0)
    

    print("offset: " + str(offset))        
    print("binary_offset: " + binary_offset)
    # print("Double check in new_img pix: (below)")
    # print(img_rgb.getpixel(0,0))

    value = (0,0,0) 

    channel1 = stringToBinary(commands[0])
    channel2 = stringToBinary(commands[1])
    channel3 = stringToBinary(commands[2])

    #check to see if commands are too big for the image
    print("Checkpoint 4")
    lenchannel1 = len(channel1)
    lenchannel2 = len(channel2)
    lenchannel3 = len(channel3)
    pixelsAvailable = width*height - offset
    if( lenchannel1 > pixelsAvailable or lenchannel2 > pixelsAvailable or lenchannel3 > pixelsAvailable):
        print("Error: Commands are too long for picture!")
        return 0

    #Writes the bits into picture
    print("Checkpoint 5")
    i = x
    j = y  
    iterator = 0
    while(i < width):
        while(j < height):
            if len(channel1) != 0 and iterator < len(channel1):
                if(channel1[iterator] == '0'):
                    evenRGB(1,i,j)
                else:
                    oddRGB(1,i,j)
            if len(channel2) != 0 and iterator < len(channel2):
                if(channel2[iterator] == '0'):
                    evenRGB(2,i,j)
                else:
                    oddRGB(2,i,j)
            if len(channel3) != 0 and iterator < len(channel3):
                if(channel3[iterator] == '0'):
                    evenRGB(3,i,j)
                else:
                    oddRGB(3,i,j)               
            iterator = iterator + 1               
            j = j + 1
        j = 0
        i = i + 1

    print("Checkpoint 6")
    img_name = "{}_diniFall.jpg".format(iid)
    new_img.save(('/Users/justinwong/Documents/GitHub/c2-server/c2/images/' + img_name), format="JPEG") #change to make it whoevers computer
    return 0



def main():

        #print("width: {}".format(x))
        #print("height: {}".format(y))

    commands = ["Hello","World","Pizza"]
    empty = ["","",""]
    print(commands)
    img = "joe.jpg"
    encodeImage(commands, img, 12)

    # ifSame = (open("joe.jpg","rb").read() == open("12_dinifall.jpg","rb").read())
    # print("Are these two images the same? ")
    # print(ifSame)

if __name__ == "__main__":
    main()
