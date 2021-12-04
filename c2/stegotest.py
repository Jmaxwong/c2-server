from PIL import Image
import random



#NOTE**** IT IS (col,row) NOT (row,col)
def encode(commands, img, iid):  # img is string of file ("diniFall.png") and commands is expected to be arr size 3
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


        offset = random.randint(3, 31)  # endpoints are included
        # starting pixel position for offset
        (x, y) = ((offset % width), (int)(offset/width))
        #col,row

        # TODO: 2nd and third pixel rgb conversion

        i = x
        j = y  # this weird code is to make sure it starts at right column and loops correctly
        value = (0,0,0) 

        #TODO: make sure offset does not exceed the image size

        while(i < width):
            while(j < height):
                if(finishedWriting(commands)):
                    isWriting = False
                    #TODO: convert char to decimal to binary

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
        # img.show()
        # print("test")
        # print(img.size)
        (x, y) = img.size
        print("width: {}".format(x))
        print("height: {}".format(y))

        # (r,g,b) = img_rgb.getpixel(0,0)
        # print(r)
        # print(g)
        # print(b)
        # print(img_rgb.getpixel(0,0))

        commands = ["yikes","ayy","pizza"]
        empty = ["","",""]
        print(finishedWriting(commands))
        print(finishedWriting(empty))

        commands[0] = commands[0][1:]
        print(commands[0])
    except:
        print("Image file not found!")


if __name__ == "__main__":
    main()
