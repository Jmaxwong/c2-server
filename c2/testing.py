import random
from bitstring import BitArray



def main():
    print("Hello World")
    width = 200
    height = 200
    command = "hello xd"

    offset = random.randint(2, (width*height))#endpoints are included
    offsetpos = ((int)(offset/width), (offset%width)) #pixel position for offset
    offset_byte = offset.to_bytes(2,"little")
    print(offset_byte)

    #c = BitArray(hex= offset_byte)
    #print(c.bin)
    print(offset_byte)


if __name__ == "__main__":
    main()