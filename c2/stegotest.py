from PIL import Image

def main():
    print("Hello World")

    try:
        img = Image.open("img.jpg")
        print(img.size)
        (x,y) = img.size
        print("width: {}".format(x))
        print("height: {}".format(y))
        for i in range(x):
            for j in range(y):
                (r,g,b) = img.getpixel((i,j))
                print("Pos ({},{}) R:{} G:{} B:{}".format(i,j,r,g,b))

                #this is how to change the rgb value of an image:
                #value = (10,10,10)#whatever rgb value you want to change
                #img.putpixel((i,j), value)

    except:
        print("Image file not found!")


if __name__ == "__main__":
    main()