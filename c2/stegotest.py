from PIL import Image
import random


def evenRGB():
    return random.randrange(0, 256, 2)
def oddRGB():
    return random.randrange(1, 257, 2)


def encode(commands, img, iid):  # img is string of file ("diniFall.png") and commands is expected to be arr size 3
    try:
        img = Image.open(img)
        img_rgb = img.convert("RGB")
        (width, height) = img.size
        # print("width: {}".format(width))
        # print("height: {}".format(height))

        #(r, g, b) = img_rgb.getpixel((0, 0))

        new_img = img.copy()

        num_commands = 0
        if(commands[0] == ""):
            return 0
        elif(commands[1] == ""):
            value = (oddRGB(), evenRGB(), evenRGB())
            new_img.putpixel((0, 0), value)
            num_commands = 1
        elif(commands[2] == ""):
            value = (oddRGB(), oddRGB(), evenRGB())
            new_img.putpixel((0, 0), value) 
            num_commands = 2        
        else:
            value = (oddRGB(), oddRGB(), oddRGB())
            new_img.putpixel((0, 0), value)
            num_commands = 3


        offset = random.randint(3, 31)  # endpoints are included
        # starting pixel position for offset
        (x, y) = ((int)(offset/width), (offset % width))

        #offset_byte = offset.to_bytes(2, "little")
        # TODO: 2nd and third pixel rgb conversion



        i = x
        j = y  # this weird code is to make sure it starts at right column and loops correctly
        value = (0,0,0) 

        #TODO: make sure offset does not exceed the image size

        while(i < height):
            while(j < width):
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
