def Handle(error, etapa): #Crash handler
    
    #To com sono, e esse handler ta uma bagunça
    #É bom dar uma ajeitada nele depois :D
    
    from colorama import Fore, init
    import os
    init()

    print(Fore.RED + "Um erro ocorreu durante a execução da maid!")
    print("Erro:", error)
    print("Criando log de crash...")
    
    import sys      
    import uuid
    import platform
    import traceback
    from datetime import datetime, date
    from config import path
    from contextlib import redirect_stdout
    
    d = datetime.now()
    
    if os.path.isdir(f'{path}/Userdata/Maid/Crash_logs') == False: #Cria diretório para os logs
        os.mkdir(f'{path}/Userdata/Maid/Crash_logs')
        
    file = '{}/Userdata/Maid/Crash_logs/Crash_log-{}-{}.txt'.format(path, d.date(), uuid.uuid4())
    
    with open(file, 'w') as crashlog:
        with redirect_stdout(crashlog):
            print("""
Um erro ocorreu durante a execução da maid
                        
Data: {}
Hora: {}
Etapa: {}
Sistema: {}
Erro: {}
    
Traceback:
    
{}""".format(date.today(), d.time(), etapa, platform.system(), error, traceback.format_exc()))
    
    print(f"Log criado com sucesso! Salvo em \"{path}/Maid/Crash_Logs\"")
    while True:
        cmd = input("Deseja reiniciar a maid (1), ou fechar a maid (2)? ")
        
        if cmd == '1':
            print(Fore.RESET)
            if platform.system() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif cmd == '2':
            sys.exit("Fechando a maid...")
        else:
            print("Comando invalido")