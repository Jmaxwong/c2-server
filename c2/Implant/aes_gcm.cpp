#include "aes_gcm.h"
#include <ostream>
#include <iostream>


AESGCM:: ~AESGCM(){
    Cleanup();
}

// Freebie: initialize AES class
AESGCM::AESGCM( BYTE key[AES_256_KEY_SIZE]){
    hAlg = 0;
    hKey = NULL;

    // create a handle to an AES-GCM provider
    nStatus = ::BCryptOpenAlgorithmProvider(
        &hAlg, 
        BCRYPT_AES_ALGORITHM, 
        NULL, 
        0);
    if (! NT_SUCCESS(nStatus))
    {
        wprintf(L"**** Error 0x%x returned by BCryptOpenAlgorithmProvider\n", nStatus);
        Cleanup();
        return;
    }
    if (!hAlg){
        wprintf(L"Invalid handle!\n");
    }
    nStatus = ::BCryptSetProperty(
        hAlg, 
        BCRYPT_CHAINING_MODE, 
        (BYTE*)BCRYPT_CHAIN_MODE_GCM, 
        sizeof(BCRYPT_CHAIN_MODE_GCM), 
        0);
    if (!NT_SUCCESS(nStatus)){
         wprintf(L"**** Error 0x%x returned by BCryptGetProperty ><\n", nStatus);
         Cleanup();
         return;
    }
    //        bcryptResult = BCryptGenerateSymmetricKey(algHandle, &keyHandle, 0, 0, (PUCHAR)&key[0], key.size(), 0);

    nStatus = ::BCryptGenerateSymmetricKey(
        hAlg, 
        &hKey, 
        NULL, 
        0, 
        key, 
        AES_256_KEY_SIZE, 
        0);
    if (!NT_SUCCESS(nStatus)){
        wprintf(L"**** Error 0x%x returned by BCryptGenerateSymmetricKey\n", nStatus);
        Cleanup();
        return;
    }
    DWORD cbResult = 0;
     nStatus = ::BCryptGetProperty(
         hAlg, 
         BCRYPT_AUTH_TAG_LENGTH, 
         (BYTE*)&authTagLengths, 
         sizeof(authTagLengths), 
         &cbResult, 
         0);
   if (!NT_SUCCESS(nStatus)){
       wprintf(L"**** Error 0x%x returned by BCryptGetProperty when calculating auth tag len\n", nStatus);
   }

   
}


void AESGCM::Decrypt(BYTE* nonce, size_t nonceLen, BYTE* data, size_t dataLen, BYTE* macTag, size_t macTagLen){

    BCRYPT_AUTHENTICATED_CIPHER_MODE_INFO authInfo;

    BCRYPT_INIT_AUTH_MODE_INFO(authInfo);

    authInfo.pbNonce = (PUCHAR) nonce;
    authInfo.cbNonce = nonceLen;
    // authInfo.pbAuthData = NULL;
    // authInfo.cbAuthData = 0;
    authInfo.pbTag = (PUCHAR) macTag;
    authInfo.cbTag = macTagLen;
    // wprintf(L"%zu %zu\n", nonceLen, macTagLen);
    //
    new_tag = new BYTE[authTagLengths.dwMaxLength];
    // wprintf(L"tag length = %d\n", authTagLengths.dwMaxLength);
    authInfo.pbMacContext = new_tag;
    authInfo.cbMacContext = authTagLengths.dwMaxLength;


    nStatus = ::BCryptDecrypt(
        hKey,
        data, // pbInput ; address of a buffer w/ the ciphertext
        dataLen, // cbInput ; bytes in the pbInput buffer to decrypt
        &authInfo, //pPaddingInfo
        NULL, //pbIV
        0, //cbIV
        NULL, // pbOutput ; output buffer
        0, // cbOutput ; size of the output
        &ptBufferSize, // *pcbResult
        0
    );

    if (!NT_SUCCESS(nStatus)){
        wprintf(L"**** Yo ignore me Error 0x%x returned by BCryptDecrypt 1\n", nStatus);
        Cleanup();
        return;
    }

    plaintext = new BYTE[ptBufferSize];
     
    DWORD ptResultSize = 0;

    // wprintf(L"BEFORE DECRYPT 2\n");
    nStatus = ::BCryptDecrypt(
        hKey,
        data, // pbInput ; address of a buffer w/ the ciphertext
        dataLen, // cbInput ; bytes in the pbInput buffer to decrypt
        &authInfo, //pPaddingInfo
        NULL, //pbIV
        0, //cbIV
        plaintext, // pbOutput ; output buffer
        ptBufferSize, // cbOutput ; size of the output
        &ptResultSize, // *pcbResult
        0
    );
    // wprintf(L"AFTER DECRYPT 2\n");

    if (!NT_SUCCESS(nStatus)){
        wprintf(L"**** Error 0x%x returned by BCryptDecrypt 2\n", nStatus);
        Cleanup();
        return;
    }

    return;

}

void AESGCM::Encrypt(BYTE* nonce, size_t nonceLen, BYTE* data, size_t dataLen){
    BCRYPT_AUTHENTICATED_CIPHER_MODE_INFO authInfo;

    BCRYPT_INIT_AUTH_MODE_INFO(authInfo);

    authInfo.pbNonce = nonce;
    authInfo.cbNonce = nonceLen;
    // authInfo.pbAuthData = NULL;
    // authInfo.cbAuthData = 0;
    // printf("authTagLength = %d\n", authTagLengths.dwMaxLength);
    tag = new BYTE[authTagLengths.dwMaxLength];
    authInfo.pbTag = tag;
    authInfo.cbTag = authTagLengths.dwMaxLength;
    // authInfo.dwFlags = 0;

    // ctBufferSize = dataLen;
    // ciphertext = new BYTE[ctBufferSize];

    nStatus = ::BCryptEncrypt(
        hKey,
        data,
        dataLen,
        &authInfo,
        NULL,
        0,
        NULL,
        0,
        &ctBufferSize,
        0
    );
    // wprintf(L"AFTER ENCRYPT 1\n");

    if (!NT_SUCCESS(nStatus)){
        wprintf(L"**** Error 0x%x returned by BCryptEncrypt 1\n", nStatus);
        Cleanup();
        return;
    }

    ciphertext = new BYTE[ctBufferSize];

    // wprintf(L"ctBufferSize = %d\n", ctBufferSize);

    DWORD ctResultSize = 0;

    nStatus = ::BCryptEncrypt(
        hKey,
        data,
        dataLen,
        &authInfo,
        NULL,
        0,
        ciphertext,
        ctBufferSize,
        &ctResultSize,
        0
    );
    // wprintf(L"AFTER ENCRYPT 2\n");

    if (!NT_SUCCESS(nStatus)){
        wprintf(L"**** Error 0x%x returned by BCryptEncrypt 2\n", nStatus);
        Cleanup();
        return;
    }

    return;

}

void AESGCM::Cleanup(){
    if(hAlg){
        ::BCryptCloseAlgorithmProvider(hAlg,0);
        hAlg = NULL;
    }
    if(hKey){
        ::BCryptDestroyKey(hKey);
        hKey = NULL;
    }
    if(tag){
          delete[] tag;
          tag = NULL;
    }
    if(ciphertext){
        delete[] ciphertext;
        ciphertext = NULL;
    }
    if(plaintext){
        delete[] plaintext;
        plaintext = NULL;
    }
    if(new_tag){
        delete[] new_tag;
        new_tag = NULL;
    }

}
