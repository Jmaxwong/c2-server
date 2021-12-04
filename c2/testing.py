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
    # offsetpos = ((int)(offset/width), (offset%width)) #pixel position for offset
    # offset_byte = offset.to_bytes(6,"little")
    # print(offset_byte)

    # print("offset number: {}".format(offset))
    # print("offset byte: {}".format(offset_byte))
    # print(offset_byte.decode('UTF-8'))

    binary = bin(2)
    binary = binary[2:]
    print("binary: " + binary)

    for j in range(1,7):
        print(j)

    if (len(binary) < 6):#pad the zeros
            for i in range(len(binary),6):
                binary = "0"+ binary

    print(binary)

    iid = 102
    img_name = "{}_diniFall.jpg".format(iid)
    print("img_name: " + img_name)

    tester = "I am a test string!"
    print(tester.encode('ascii'))


if __name__ == "__main__":
    main()