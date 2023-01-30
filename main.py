from status import GetStatus

def loop():
    
    i = input("Run or Config? ")

    if(i == 'config'):
        wpp.config()
    elif(i == 'run'):
        wpp.run(input("Number to check: "))
    loop()

wpp = GetStatus()
loop()