#include <windows.h>
#include <string>
#include <iostream>
#include <winhttp.h>


std::string makeHttpRequest(std::wstring fqdn, int port, std::wstring uri, bool useTLS,
    std::wstring optional_headers, std::wstring wszVerb, std::string http_data){

    std::string result = "";
    // std::wcout << "fqdn: " << fqdn << "      port: " << port << std::endl;

    // setting the user-agent
    LPCWSTR userAgent = reinterpret_cast<LPCWSTR>(L"Myles920");

    // Initialization of the WinHttp Session.
    HINTERNET sessionHandle = WinHttpOpen(userAgent, WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, NULL, NULL, 0);
    // std::wcout << "session handle made!" << std::endl;

    // Configuring the HTTP client
    HINTERNET connectHandle = WinHttpConnect(sessionHandle, fqdn.c_str(), port, 0);
    // std::wcout << "connect handle made!" << std::endl;

    // Opening the http request
    HINTERNET openRequestHandle = NULL;

    if (useTLS ) { //removed code "&& port == 443"
        openRequestHandle = WinHttpOpenRequest(connectHandle, L"POST", uri.c_str(),
            NULL, NULL, WINHTTP_DEFAULT_ACCEPT_TYPES, WINHTTP_FLAG_SECURE | WINHTTP_FLAG_BYPASS_PROXY_CACHE);
        // std::wcout << "openRequest handle made!" << std::endl;
        // std::wcout << L"Error: " << GetLastError() << std::endl;
    }
    else if (!useTLS ) { // removed code "&& port == 80"
        openRequestHandle = WinHttpOpenRequest(connectHandle, L"POST", uri.c_str(), 
            NULL, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, WINHTTP_FLAG_BYPASS_PROXY_CACHE);
        // std::wcout << "openRequest handle made!" << std::endl;
        // std::wcout << L"Error: " << GetLastError() << std::endl;
    }
    else {
        WinHttpCloseHandle(connectHandle);
        // std::wcout << "connect handle closed!" << std::endl;
        WinHttpCloseHandle(sessionHandle);
        // std::wcout << "session handle closed!" << std::endl;

        return result;
    }

    

    // setting options to ignore security flags
    DWORD options = SECURITY_FLAG_IGNORE_UNKNOWN_CA | SECURITY_FLAG_IGNORE_CERT_DATE_INVALID | SECURITY_FLAG_IGNORE_CERT_CN_INVALID | SECURITY_FLAG_IGNORE_CERT_WRONG_USAGE;
    LPVOID optionBuffer = &options;
    DWORD optionBufferLength = sizeof(DWORD);

    WinHttpSetOption(openRequestHandle, WINHTTP_OPTION_SECURITY_FLAGS, optionBuffer, optionBufferLength);

    // sending request
    // std::wcout << L"http_data len = " << wcslen(http_data.c_str()) << std::endl;
    // std::wcout << L"http_data = " << (LPCWSTR) http_data.c_str() << std::endl;
    // std::wcout << L"optional_headers len = " << wcslen(optional_headers.c_str()) << std::endl;
    if ( WinHttpSendRequest(
            openRequestHandle, 
            optional_headers.c_str(), 
            -1, 
            (LPVOID) http_data.c_str(),
            (DWORD) http_data.length(),
            (DWORD) http_data.length(),
            0 )
        ){
        // Receiving the data and reading it all.
        if (WinHttpReceiveResponse(openRequestHandle, NULL)) {
            if (WinHttpQueryDataAvailable(openRequestHandle, NULL)) {
                char readBufferTemp[4096];
                LPVOID readBuffer = &readBufferTemp;
                unsigned long bytesRead;

                std::wcout << "starting to read data!" << std::endl;

                do {
                    bytesRead = 0;
                    std::wcout << "Read some data..." << std::endl;
                    if (WinHttpReadData(openRequestHandle, readBuffer, 4096, &bytesRead) == false) {
                        std::wcout << "failed to read." << std::endl;
                        break;
                    }
                    // std::istringstream is( bytesRead );
                    // unsigned long test = std::strtoul( bytesRead, NULL, 0 );
                    // std::wcout << "bytesRead = " << bytesRead << std::endl;

                    // std::wcout << test << std::endl;
                    // unsigned int bytesReadActual = (int)test;
                    // std::wcout << bytesReadActual << std::endl;
                    if (bytesRead != 0) {
                        std::string tempData(&readBufferTemp[0], &readBufferTemp[bytesRead]);
                    
                        std::cout << "tempData = " << tempData << std::endl;
                        result.append(tempData);
                    }
                } while (bytesRead != 0);
            }
            else{std::wcout << L"Failed at query data available" << std::endl;}
        }
        else{std::wcout << L"Failed at receive response" << std::endl;}
    }
    else{
        std::wcout << L"Failed at sending request" << std::endl;
        std::wcout << L"Error: " << GetLastError() << std::endl;
    }

    WinHttpCloseHandle(openRequestHandle);
    // std::wcout << "openRequest handle closed!" << std::endl;
    WinHttpCloseHandle(connectHandle);
    // std::wcout << "connect handle closed!" << std::endl;
    WinHttpCloseHandle(sessionHandle);
    // std::wcout << "session handle closed!" << std::endl;

    std::cout << result << std::endl;


    // Prints any errors
    // if (result.length() == 0){
    //     printf( "Error %d has occurred.\n", GetLastError());
    // }

    // std::wcout << "At least we got to the end :p" << std::endl;
    
    return result;
}

// int wmain(int argc,  wchar_t* argv[]){
//     if(argc !=5){
//         std::wcout << L"Incorrect number of arguments: you need 4 positional arguemts" << std::endl;
//         return 0;
//     }

//     std::wstring fqdn = std::wstring(argv[1]);
//     int port = std::stoi( argv[2] );
//     std::wstring uri = std::wstring(argv[3]);
//     int  useTLS =std::stoi(argv[4]);
//     bool tls;
//     if (useTLS == 1){
//         tls = true;
//     } else if (useTLS == 0){
//         tls = false;

//     } else{
//         std::wcout << L"bad value for useTls" << std::endl;
//         return 0;
//     }
//      std::wcout << makeHttpRequest(fqdn,  port, uri, tls) << std::endl;
//     return 0;
    
// }