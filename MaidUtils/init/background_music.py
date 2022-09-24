def Play(): #Toca uma musica de fundo quando a maid é iniciada (caso esteja como true na config principal)
    from colorama import Fore, init
    from config import path
    import configparser
    init()
    
    import contextlib
    with contextlib.redirect_stdout(None): #Importa o pygame com o stdout redirecionado para None
        import pygame                      #Para ele não mostrar a mensagem de import no terminal
    
    print(Fore.CYAN + "Iniciando música..." + Fore.RESET)
    
    config = configparser.ConfigParser()
    config.read(f"{path}/Userdata/Configurações/Principal.ini")    
    diretorio = config.get('Geral', 'background-music-path')
    volume = config.get('Geral', 'background-music-volume')
    loop = config.get('Geral', 'background-music-loop')

    if loop.isdigit() == False:
        print(Fore.RED + "O valor do loop é invalido (deve apenas conter números e traços). Usando valor padrão..." + Fore.RESET)
        loop = -1  
        
    loop= int(loop)
    volume = float(volume)
    try:
        pygame.init()                                                #Iniciando pygame 
        pygame.mixer.init()                                          #Iniciando mixer
        pygame.mixer.music.load(diretorio)                           #Carregando musica
        pygame.mixer.music.set_volume(volume)                        #Muda o volume do audío
        pygame.mixer.music.play(loop)                                #Tocando audio
        while pygame.mixer.music.get_busy():                         #Espera o audio tocar para destruir o objeto
            pygame.time.Clock().tick(10)                             #Esperando...
        pygame.mixer.music.unload()                                  #Descarregando arquivo
        pygame.mixer.music.stop()                                    #Encerrando mixer     
    except Exception as x:
        print(Fore.RED + "Um erro ocorreu com a música de fundo!")
        print("Certifique-se que o diretório da música foi inserido corretamente e tente novamente.")
        print(f"Erro: {x}" + Fore.RESET)
        