import donut


shellcode = donut.create(
    file="hello.exe", url='https://127.0.0.1/', format=2, bypass=3)
