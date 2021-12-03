#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <math.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image/stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image/stb_image_write.h"

// For now, only change value of R from RGB
void change_even_odd(int pixels_to_change, unsigned char *image, bool toEven, size_t image_size, int channels, unsigned char *alter_image){
    int cur_pixel = 0;

    for(unsigned char *p = image, *pa = alter_image; p != image + image_size && cur_pixel < pixels_to_change; p += channels, pa += channels){
        if(*p == 0 && toEven){
            *pa = 0;
            *(pa + 1) = *(p + 1);
            *(pa + 2) = *(p + 2);
        }else if(*p == 0){
            *pa = 1;
            *(pa + 1) = *(p + 1);
            *(pa + 2) = *(p + 2);
        }else if(toEven){
            if(((*p)%2) == 0 ){
                *(pa) = *(p);
                *(pa + 1) = *(p + 1);
                *(pa + 2) = *(p + 2);
            }else{
                *(pa) = (*(p)) - 1;
                *(pa + 1) = *(p + 1);
                *(pa + 2) = *(p + 2);
            }
        }else{
            if(((*p)%2) == 0 ){
                *(pa) = (*(p)) - 1;
                *(pa + 1) = *(p + 1);
                *(pa + 2) = *(p + 2);
            }else{
                *(pa) = *(p);
                *(pa + 1) = *(p + 1);
                *(pa + 2) = *(p + 2);
            }
        }
        cur_pixel++;
    }
}

int binary_to_decimal(char* n, int size){
    int returnDecimal = 0;
    for(int x = 0; x < size; x++){
        if(*(n + x) == '1'){
            returnDecimal += pow(2, (size-x-1));
        }
    }
    return returnDecimal;
}

//this function assumes the char* messages are divisible by 7 bits
char* binary_to_ASCII(char* message, int max_size){
    int msgTraverse = 0;
    int count0 = 0;
    char *returnASCII = new char[(max_size/7)];
    char *toConvert = new char[7];
    for(int iteration = 0; count0 != 7; iteration++){
        if(msgTraverse == 7){
            msgTraverse = 0;
            count0 = 0;
        }
        toConvert[msgTraverse] = message[iteration];
        if(message[iteration] == '0'){
            count0++;
        }else{
            count0 = 0;
        }
        if(msgTraverse == 6){
            returnASCII[iteration/7] = (char) binary_to_decimal(toConvert, 7);
        }
        msgTraverse++;
    }
    return returnASCII;
}

char** decode_jpeg(unsigned char *image, int max_pixels, int width, int height, int channels, size_t image_size){
    //allocate space for char** that will be returned
    char **messages = new char*[3];
    char *message_1; 
    char *message_2; 
    char *message_3;

    //check first pixel and see how many char* need to be allocated memory; odd RGB value = 1 which means theres a message in the corresponding color
    unsigned char *fp = image;
    if((*fp)%2 == 1){
        message_1 = (char*) malloc(max_pixels);
        //printf("DEBUG: First Pixel R Value is Odd\n");
    }else{
        message_1 = NULL;
        //printf("DEBUG: First Pixel R Value is Even\n");
    }
    if((*(fp+1))%2 == 1){
        message_2 = (char*) malloc(max_pixels);
        //printf("DEBUG: First Pixel G Value is Odd\n");
    }else{
        message_2 = NULL;
        //printf("DEBUG: First Pixel G Value is Even\n");
    }
    if((*(fp+2))%2 == 1){
        message_3 = (char*) malloc(max_pixels);
        //printf("DEBUG: First Pixel B Value is Odd\n");
    }else{
        message_3 = NULL;
        //printf("DEBUG: First Pixel B Value is Even\n");
    }

    //check 2nd and 3rd pixels for offset
    char *offset = new char[6];
    fp += channels;
    //2nd pixel; R
    if(((*fp)%2) == 0 ){
        offset[0] = '0';
    }else{
        offset[0] = '1';
    }
    //2nd pixel; G
    if(((*(fp+1))%2) == 0 ){
        offset[1] = '0';
    }else{
        offset[1] = '1';
    }
    //2nd pixel; B
    if(((*(fp+2))%2) == 0 ){
        offset[2] = '0';
    }else{
        offset[2] = '1';
    }
    fp += channels;
    //3rd pixel; R
    if(((*fp)%2) == 0 ){
        offset[3] = '0';
    }else{
        offset[3] = '1';
    }
    //3rd pixel; G
    if(((*(fp+1))%2) == 0 ){
        offset[4] = '0';
    }else{
        offset[4] = '1';
    }
    //3rd pixel; B
    if(((*(fp+2))%2) == 0 ){
        offset[5] = '0';
    }else{
        offset[5] = '1';
    }

    //std::cout << "DEBUG: Offset value (binary) is: " << offset << std::endl;
    //convert binary offset to decimal offset
    int int_offset = binary_to_decimal(offset, 6);
    //std::cout << "DEBUG: Offset value (decimal) is: " << int_offset << std::endl;

    //error checking: return null if offset value exceeds number of pixels in picture
    if(int_offset > (max_pixels - 3)){
        std::cout << "DEBUG: offset value exceeds number of pixels" << std::endl;
        return NULL;
    }

    //Read from image starting from offset pixel
    //NOTE: min_offset is 0 which refers to the very first pixel
    //      i.e. if offset is 23, then start reading from the 24th pixel
    //      if things go well on encoding side, offset should never be 0, 1, or 2
    //Assumption: ASCII characters only uses 7 bits; offset pixel contains the first bit of the first ASCII character of the message(s)
    int relative_pixel = 0;
    int message_1_0counter = 0;
    int message_2_0counter = 0;
    int message_3_0counter = 0;
    for(unsigned char *p = (image + (int_offset * channels)); p != image + image_size; p += channels){
        if(message_1 != NULL && message_1_0counter != 7){
            if(((*p)%2) == 0 ){
                message_1[relative_pixel] = '0';
                message_1_0counter++;
            }else{
                message_1[relative_pixel] = '1';
                message_1_0counter = 0;
            }
        }
        if(message_2 != NULL && message_2_0counter != 7){
            if(((*(p+1))%2) == 0 ){
                message_2[relative_pixel] = '0';
                message_2_0counter++;
            }else{
                message_2[relative_pixel] = '1';
                message_2_0counter = 0;
            }
        }
        if(message_3 != NULL && message_3_0counter != 7){
            if(((*(p+2))%2) == 0 ){
                message_3[relative_pixel] = '0';
                message_3_0counter++;
            }else{
                message_3[relative_pixel] = '1';
                message_3_0counter = 0;
            }
        }
        relative_pixel++;
        if(relative_pixel % 7 == 0){
            if(message_1_0counter != 7){
                message_1_0counter = 0;
            }
            if(message_2_0counter != 7){
                message_2_0counter = 0;
            }
            if(message_3_0counter != 7){
                message_3_0counter = 0;
            }
        }
        //TODO: error checking: return null if reach the end of picture without ever reading an ASCII null character
    }

    //convert binary messages into ASCII characters
    if(message_1 != NULL){
        message_1 = binary_to_ASCII(message_1, max_pixels);
    }
    if(message_2 != NULL){
        message_2 = binary_to_ASCII(message_2, max_pixels);
    }
    if(message_3 != NULL){
        message_3 = binary_to_ASCII(message_3, max_pixels);
    }

    //assign char* messages to the return char**
    messages[0] = message_1;
    messages[1] = message_2;
    messages[2] = message_3;

    //cleanup
    delete(offset);
    free(message_1);
    free(message_2);
    free(message_3);

    return messages;
}

int main(int argc, char *argv[]){

    // Make sure correct number of arguments
    if(argc != 2){
        printf("Incorrect number of arguments: you need 2 positonal arguemts");
        return 0;
    }

    // Initialize width, height, and channels for original image
    int width, height, channels;
    unsigned char *img = stbi_load("Doge.jpg", &width, &height, &channels, 0);
    if(img == NULL){
        printf("RIP for image loading");
        return 0;
    }
    printf("Image loaded with width: %dpx, height: %dpx, and channels: %d\n", width, height, channels);

    size_t img_size = width * height * channels;

    // Allocate memory for altered jpeg
    int altered_img_channels = 3;
    size_t altered_img_size = width * height * altered_img_channels;
    unsigned char *altered_img = (unsigned char*) malloc(altered_img_size);
    if(altered_img == NULL){
        printf("RIP for memory allocation for altered img");
        return 0;
    }

    // Perform pixel manipulation; img_size/3 is the entire image since there are 3 channels (works)
    // change_even_odd(img_size/3, img, true, img_size, channels, altered_img);

    // Print out RGB values for original img
    int pixel_num = 0;
    for(unsigned char *p = img; p != img + img_size; p += channels, pixel_num ++){
        printf("Pixel at %d height, %d width, R: %d, G: %d, B: %d\n", pixel_num / height, pixel_num % height, *(p), *(p + 1), *(p + 2));
    }

    printf("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");

    int max_pixels = width * height;
    std::cout << "Max Pixels: " << max_pixels << std::endl;

    char **messages = new char*[3];
    messages = decode_jpeg(img, max_pixels, width, height, channels, img_size);

    if(messages[0]){
        std::cout << "Message 1: " << messages[0] << std::endl;
    }else{
        std::cout << "There is no message 1" << std::endl;
    }
    if(messages[1]){
        std::cout << "Message 2: " << messages[0] << std::endl;
    }else{
        std::cout << "There is no message 2" << std::endl;
    }
    if(messages[2]){
        std::cout << "Message 3: " << messages[0] << std::endl;
    }else{
        std::cout << "There is no message 3" << std::endl;
    }



    // Print out RGB values for altered img (works)
    // int pixel_num2 = 0;
    // for(unsigned char *pa = altered_img; pa != altered_img + altered_img_size; pa += altered_img_channels, pixel_num2 ++){
    //     printf("Pixel2 at %d height, %d width, R: %d, G: %d, B: %d\n", pixel_num2 / height, pixel_num2 % height, *(pa), *(pa + 1), *(pa + 2));
    // }


    // Convert to gray (works)
    // int gray_channels = 1;
    // size_t gray_img_size = width * height * gray_channels;
    // // Allocate memory for gray image
    // unsigned char *gray_img = (unsigned char*) malloc(gray_img_size);
    // if(gray_img == NULL){
    //     printf("RIP for memory allocation for gray img");
    //     return 0;
    // }


    // Loop over all pixels of jpeg
    // for(unsigned char *p = img, *pg = gray_img; p != img + img_size; p += channels, pg += gray_channels){
    //     *pg = (uint8_t)((*p + *(p + 1) + *(p + 2))/3.0);
    // }

    // stbi_write_jpg("Doge2.jpg", width, height, gray_channels, gray_img, 100);

    //cleanup
    delete(messages);
    stbi_image_free(altered_img);
    stbi_image_free(img);
}