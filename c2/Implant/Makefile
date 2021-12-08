CC=gcc
CXX=g++
CFLAGS= -Wall
LDFLAGS= -lcrypt32 -lbcrypt -municode -lwinhttp
PDB=-g
BIN=bin
ifeq ($(OS),Windows_NT)
	RM=powershell /c rm
else
	RM=rm
endif
all: adversary

adversary:
	$(CXX) final_proj.cpp $(CFLAGS) $(LDFLAGS) -o LMAOware.exe 
	
safe:
	$(CXX) final_proj_safe.cpp $(CFLAGS) $(LDFLAGS) -o safe_implant.exe 

clean:
	$(RM) *.exe
#g++   .\pathutils.cpp .\aes_gcm.cpp  sqlite3.o -municode -static -lshell32  -lshlwapi -lcrypt32 -lbcrypt -O3