from PIL import Image
import random



#NOTE**** IT IS (col,row) NOT (row,col)
def encodeImage(commands, img, iid):  # img is string of file ("diniFall.png") and commands is expected to be arr size 3
    try:
        img = Image.open(img)
        img_rgb = img.convert("RGB")
        (width, height) = img.size
        # print("width: {}".format(width))
        # print("height: {}".format(height))

        #(r, g, b) = img_rgb.getpixel((0, 0))

        new_img = img.copy()

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

        offset = random.randint(3, 63)  # endpoints are included #edward shoudnt this be 63??
        # starting pixel position for offset


        while (offset > (width*height)):
            print("ERROR: INVALID OFFSET GENERATED")
            print("Offset: " + offset)
            offset = random.randint(3, 63)     


        #TODO: check to see if commands are too big for the image     

        
        (x, y) = ((offset % width), (int)(offset/width))

        #done TODO: 2nd and third pixel rgb conversion
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
        
        print("offset: " + offset)        
        print("binary_offset: " + binary_offset)
        print("Double check in new_img pix: ")
        print(img_rgb.getpixel(0,0))

        i = x
        j = y  # this weird code is to make sure it starts at right column and loops correctly
        value = (0,0,0) 

        #TODO: convert char to decimal to binary
        #ord(num)


        


        while(i < width):
            while(j < height):
                

                #TODO: add the null byte                 
                j = j + 1
            j = 0
            i = i + 1
        img_name = "{}_diniFall.jpg".format(iid)
        new_img.save(img_name, format="jpg")
    except:
        print("no file found")

    return 0



def main():
    try:
        img = Image.open("minireeves.png")
        img_rgb = img.convert("RGB")
        (x, y) = img.size
        print("width: {}".format(x))
        print("height: {}".format(y))

        commands = ["yikes","ayy","pizza"]
        empty = ["","",""]

        commands[0] = commands[0][1:]
        print(commands[0])
    except:
        print("Image file not found!")


if __name__ == "__main__":
    main()
