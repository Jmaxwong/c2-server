import random
from bitstring import BitArray



def main():
    #test = 50000000
    #test2 = test.to_bytes(6,"little")


    width = 200
    height = 200
    command = "hello xd"
    num_pixels = width * height
    offset = random.randint(2, num_pixels)#endpoints are included
    offsetpos = ((int)(offset/width), (offset%width)) #pixel position for offset
    offset_byte = offset.to_bytes(6,"little")
    print(offset_byte)

    print("offset number: {}".format(offset))
    print("offset byte: {}".format(offset_byte))
    print(offset_byte.decode('UTF-8'))



if __name__ == "__main__":
    main()