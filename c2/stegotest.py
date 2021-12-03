from PIL import Image
import random

def evenRGB():
    return random.randrange(0,256,2)

def oddRGB():
    return random.randrange(1,257,2)


def encode(commands, img):#img is string of file ("diniFall.png")
    try:
        img = Image.open(img)
        img_rgb = img.convert("RGB")
        (width,height) = img.size
        # print("width: {}".format(width))
        # print("height: {}".format(height))

        (r,g,b) = img_rgb.getpixel((0,0))

        newimg = img.copy()
        numCommands = len(commands)
        #channels = []

        if numCommands == 1:
            value = (oddRGB(), evenRGB(), evenRGB())
            newimg.putpixel((0,0),value)

        elif numCommands == 2:
            value = (oddRGB(), oddRGB(), evenRGB())
            newimg.putpixel((0,0),value)

        elif numCommands == 3:
            value = (oddRGB(), oddRGB(), oddRGB())
            newimg.putpixel((0,0),value)  

        else:
            return 0

        #TODO: pixels 1 and 2 are offsets for the pointer
        offset = random.randint(2, (width*height))#endpoints are included
        offsetpos = ((int)(offset/width), (offset%width)) #pixel position for offset

        offset_byte = offset.to_bytes(2,"little")

        #newimg.putpixel((0,1), value)
        #newimg.putpixel((0,2), value)


        # newimg.save("newimg.png", format="png")
    except:
        print("no file found")
    return 0


def main():
    try:
        img = Image.open("minireeves.png")
        img_rgb = img.convert("RGB")
        #img.show()
        #print("test")
        #print(img.size)
        (x,y) = img.size
        print("width: {}".format(x))
        print("height: {}".format(y))
        pixel = img_rgb.getpixel((25,26))
        print(pixel)
        print(img_rgb.getpixel((64,64)))
        print(img_rgb)

        newimg = img.copy()
        #newimg.save("newimg.png", format="png")

        # for i in range(y):
        #     for j in range(x):
        #         (r,g,b) = img_rgb.getpixel((j,i))
        #         print("Pos ({},{}) R:{} G:{} B:{}".format(i,j,r,g,b))


    except:
        print("Image file not found!")

if __name__ == "__main__":
    main()