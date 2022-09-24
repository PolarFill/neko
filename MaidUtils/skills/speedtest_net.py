def Test(): #Executa um teste de velocidade na net
    import speedtest
    import configparser
    from config import path
    from MaidUtils.init.tts import say
    from colorama import Fore, init
    init()
    
    config = configparser.ConfigParser()
    config.read(f'{path}/Userdata/Maid/Session/session.info')
    
    if config.get('Session', 'online') == 'false':  #Cancela o teste caso o usuario não tenha conexão com a internet
        say("Não foi possível estabelecer uma conexão com a internet")
    else:
        print(Fore.BLUE + "(Por motivos técnicos, esse teste pode não ter 100% de acurácia).")
        print("Iniciando teste..." + Fore.RESET)
        say("Iniciando teste...", out=False)
        
        st = speedtest.Speedtest() #Iniciando teste
        st.get_best_server()       #Pegando o melhor servidor disponível
        
        download = str(st.download())               #Teste de download
        upload = str(st.upload(pre_allocate=False)) #Teste de upload
        
        print(Fore.BLUE + f"A sua velocidade de download é: {download[:3]}MB" + Fore.RESET) #Falando velocidade de download
        say(f"A sua velocidade de download é: {download[:3]}MB", out=False)                  #Mostrando velocidade de download
        
        print(Fore.BLUE + f"A sua velocidade de upload é: {upload[:3]}MB" + Fore.RESET) #Velocidade de upload
        say(f"A sua velocidade de upload é: {upload[:3]}MB", out=False)                 #Velocidade de upload
        
        print(Fore.BLUE + f"O seu ping é: {st.results.ping}ms" + Fore.RESET) #Ping
        say(f"O seu ping é: {st.results.ping}ms", out=False)                 #Ping

        print(Fore.BLUE + "Imagem do teste: {}".format(st.results.share()) + Fore.RESET) #Imagem do teste
    