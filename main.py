###################################
###Esta é a parte onde o input da maid é pego e reconhecido
###################################
from commands import *

def eternal_input():
    from MaidUtils.init.tts import say          #Importando função do tts
    from MaidUtils.init.voice import capture    #Importando função de captura de fala

    import configparser
    from config import path
    config = configparser.ConfigParser()
    config.read([f'{path}/Userdata/Maid/Session/session.info', f'{path}/Userdata/Configurações/Principal.ini']) #Lendo configs

    use_prefix = config.get("Geral", 'usar-prefixo').lower()
    prefixo = config.get("Geral", 'prefixo').lower()
    background_music = config.get("Geral", 'background-music').lower()
    input_type = config.get("Geral", "voice").lower()
    
    if background_music == 'true': #Toca música de fundo, se configurado
        import MaidUtils.init.background_music, multiprocessing, time
        multiprocessing.Process(target=MaidUtils.init.background_music.Play).start()
        time.sleep(2)

    if input_type == "true": #Usando voz
        print("Diga o comando que deseja executar" + Fore.RESET)
    else:
        print("Digite o comando que deseja executar" + Fore.RESET)

    while True:
        if use_prefix == 'true': #Se o usuario estiver utilizando um prefixo
            cmd = capture()      #Joga pro capture
        else:                    #Caso o contrario
            cmd = prefixo        #Usa o cmd como prefixo
            
        try:
            if cmd == prefixo:
                if use_prefix != 'false':
                    say("Olá! No que posso te ajudar?")
                cmd = capture()

                if cmd == None:
                    say("Desculpe, não entendi")
                
                elif cmd in answers_print: #Copia print da tela no clipboard
                    import MaidUtils.skills.screenshot
                    MaidUtils.skills.screenshot.runSave()
                    say('Screenshot salva na pasta "Screenshots".')

                elif cmd in answers_dado: #Rola um dado
                    import MaidUtils.skills.dice
                    resultado = MaidUtils.skills.dice.roll()
                    say(f"O resultado é: {resultado}")

                elif cmd in answers_maidutils:
                    import MaidUtils.init.maidutils
                    say('Iniciando MaidUtils...')
                    MaidUtils.init.maidutils.Main()

                elif cmd.startswith('dado de '): #Rola um número definido pelo usuario
                    import MaidUtils.skills.dice, re
                    re.sub('\D', '', cmd) #Substituindo todas as letras por whitespace
                    MaidUtils.skills.dice.roll_custom(cmd)
                    say(f"O resultado é: {resultado}")
                    
                elif cmd in answers_tempnote: #Escreve uma nota temporaria
                    import MaidUtils.skills.agenda
                    say("O que deseja anotar?")
                    note = capture()
                    MaidUtils.skills.agenda.TempNote(note)
                    say("Nota temporária escrita!")
                    
                elif cmd in answers_ReadTempNote: #Lê a nota temporaria
                    import MaidUtils.skills.agenda
                    note_returned = MaidUtils.skills.agenda.ReadTempNote()
                    say(note_returned)
                    
                elif cmd in answers_speednet: #Testa velocidade da net
                    import MaidUtils.skills.speedtest_net
                    say("Aguarde...")
                    MaidUtils.skills.speedtest_net.Test()

                elif cmd in answers_sair: #Fecha a maid
                    say("Saindo...")
                    import sys
                    sys.exit("Fechando maid...")
                    
                elif cmd in answers_restart: #Reinicia maid
                    say("Reiniciando...")
                    import os, sys
                    os.execl(sys.executable, sys.executable, *sys.argv)
                    
                elif cmd in answers_window: #Manipula janela
                    import MaidUtils.skills.get_window
                    MaidUtils.skills.get_window.Manipulate()
                    
                elif cmd.startswith(tuple(answers_say)): #Faz a maid falar algo
                    if cmd in answers_say:
                        say("O que deseja que eu fale?")
                        fala = capture()
                        if fala != None:
                            say(fala)
                        else:
                            say("Desculpe, não entendi o que quis dizer.")
                    else:
                        for i in answers_say:
                            cmd = cmd.replace(i, '', 1)
                            cmd = cmd.lstrip()
                        say(cmd)
                        
                elif cmd in answers_limpar: #Limpa o terminal da maid
                    import os, platform
                    if platform.system().startswith('W'):
                        os.system('cls')
                    else:
                        os.system('clear')

                elif cmd in answers_joquempo: #Joga pedra papel tesoura
                    import MaidUtils.skills.games
                    MaidUtils.skills.games.Joquempo()
                    
                elif cmd in answers_hora:     #Fala a hora atual
                    import MaidUtils.skills.time
                    MaidUtils.skills.time.Time()
                
                elif cmd in answers_data:     #Fala a data atual
                    import MaidUtils.skills.time
                    MaidUtils.skills.time.Date()
                
                elif cmd.startswith(tuple(answers_timer)): #Executa um timer
                    import MaidUtils.skills.time, multiprocessing
                    if cmd in answers_timer:
                        say("Quanto tempo deseja configurar no temporizador?")
                        time = capture()
                        multiprocessing.Process(target=MaidUtils.skills.time.Timer, args=(time,)).start()
                    else:
                        multiprocessing.Process(target=MaidUtils.skills.time.Timer, args=(cmd,)).start()
                
                elif cmd in answers_poweroff: #Desliga, reinicia, ou desloga o pc
                    say("Deseja realmente realizar essa ação?")
                    confirm = capture()
                    if confirm == 'sim':
                        import MaidUtils.skills.poweroff
                        MaidUtils.skills.poweroff.Main(cmd)
                
                elif cmd.startswith(tuple(answers_cronômetro)): #Inicia um cronometro
                    import MaidUtils.skills.time, multiprocessing
                    if cmd in answers_timer:
                        say("Quanto tempo deseja configurar no cronômeto?")
                        time = capture()
                        multiprocessing.Process(target=MaidUtils.skills.time.Cronometro, args=(time,)).start()
                    else:
                        multiprocessing.Process(target=MaidUtils.skills.time.Cronometro, args=(cmd,)).start()
                
                elif cmd.startswith(tuple(answers_changelog)): #Changelog da maid
                    import MaidUtils.init.update
                    MaidUtils.init.update.Changelog(cmd)
                   
                elif cmd.startswith(tuple(answers_wikipedia)): #Pesquisa na wikipedia
                    import MaidUtils.skills.search
                    if cmd in answers_wikipedia: 
                        say("O que deseja pesquisar?")
                        search = capture()
                        MaidUtils.init.skills.search.Wikipedia(search, keyword=1)
                    else:
                        for i in answers_wikipedia:
                            cmd = cmd.replace(i, '', 1)
                        MaidUtils.init.skills.search.Wikipedia(cmd)
                        
                elif cmd in answers_maidrecheck:
                    import MaidUtils.init.maidutils
                    say('Aguarde...')
                    MaidUtils.init.maidutils.Recheck()
                        
                elif cmd in answers_timer:
                    if 'iniciar' in cmd:
                        import MaidUtils.skills.time, multiprocessing
                        say("Iniciando contagem...")
                        TimeCount_process = multiprocessing.Process(target=MaidUtils.skills.time.Timecount)
                        TimeCount_process.start
                    else:
                        import MaidUtils.skills.time
                        MaidUtils.skills.time.CheckTimeCount()
                    
                elif cmd in answers_cancelar: #Cancela input
                    pass
                
                elif cmd.startswith(tuple(answers_local_playlist)):
                    import MaidUtils.skills.play_songs
                    import multiprocessing
                    LocalPlaylist = multiprocessing.Process(target=MaidUtils.skills.play_songs.LocalPlay, args=(cmd,))
                    LocalPlaylist.start()
                
                ##############################################TOCAR MUSICAS E ETC
                
                elif cmd.startswith('youtube') or cmd.startswith('YouTube'): #Toca musicas do youtube
                    import multiprocessing
                    import MaidUtils.skills.play_songs
                    
                    ffmpeg = True
                    if MaidUtils.skills.play_songs.Check_ffmpeg() == False:
                        print(Fore.RED + "O ffmpeg não foi encontrado no path.")
                        print("O ffmpeg é uma ferramenta utilizada pela maid para uma melhor reprodução de musíca.")
                        print("Caso deseje instalar o ffmpeg, digite ou diga \"instalar ffmpeg\" a qualquer momento.")
                        print("Caso já tenha o ffmpeg, coloque ele no path." + Fore.RESET)
                        ffmpeg = None
                    if cmd == 'YouTube' or cmd == 'youtube':
                        link = input('Insira o link do vídeo >> ')
                        say('Aguarde...')
                        if ffmpeg == None:
                            Youtubeplay = multiprocessing.Process(target=MaidUtils.skills.play_songs.Youtube2, args=(link,)).start()
                        else:
                            Youtubeplay = multiprocessing.Process(target=MaidUtils.skills.play_songs.Youtube, args=(link,)).start()
                    else:
                        cmd.replace('YouTube ', '')
                        say('Aguarde...')
                        if ffmpeg == None:
                            Youtubeplay = multiprocessing.Process(target=MaidUtils.skills.play_songs.Youtube2, args=(cmd, 1)).start()
                        else:
                            Youtubeplay = multiprocessing.Process(target=MaidUtils.skills.play_songs.Youtube, args=(cmd, 1)).start()
                
                elif cmd == 'instalar ffmpeg':
                    import multiprocessing
                    import MaidUtils.skills.play_songs
                    say("Instalando ffmpeg...")
                    DownloadFFMPEG = multiprocessing.Process(target=MaidUtils.skills.play_songs.Install_ffmpeg)
                    DownloadFFMPEG.start()
                
                elif cmd in answers_stop_song:
                    import MaidUtils.skills.play_songs
                    check = MaidUtils.skills.play_songs.Check()
                    if check == 'youtube':
                        say("Parando youtube...")
                        Youtubeplay.kill()
                    elif check == 'spotify':
                        say("Parando spotify...")
                        SpotifyPlay.kill()
                    elif check == 'LocalPlaylist':
                        say("Parando playlist...")
                        LocalPlaylist.kill()
                    else:
                        say("Nenhuma musíca está tocando no momento")
                
                ###############################################else e exceções    

                elif maidutils_modules_activated == 'true' and cmd in maidutils_module_prefixes:
                    import MaidUtils.init.maidutils
                    MaidUtils.init.maidutils.Run(cmd, maidutils_module_names)

                else: #Fala que o input não foi reconhecido
                    say('Desculpe, não entendi.')
                    
        except TypeError: #Caso o usuario não fale nada se n me engano
            say("Desculpe, não entendi.")
        except RecursionError: #Caso o usuario fique sem falar nada por um bom tempo, atingindo o limite de
            import os, sys     #recursão
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as x: #Crash handler
            from MaidUtils.init import crash_handler #Importando crash handler
            crash_handler.Handle(x, 'Execução') #Executando

###################################
###Esta é a parte onde a maid e iniciada
###################################

if __name__ == "__main__": #Processo de inicialização da maid
    try:                                         #Pega exceções na inicialização da maid
        import sys, platform, os
        if platform.system().startswith('W'):    #Se o sistema for windows
            os.system("title Neko")              #Coloca o titulo usando title
            os.system("cls")                     #Limpa o terminal com cls
        else:                                    #Se for linux ou mac
            sys.stdout.write("\x1b]2;Neko\x07")  #Coloca o titulo usando escape codes
            os.system("clear")                   #Limpa o terminal com clear
        
        from colorama import Fore, init
        init()

        from config import analyze_conditions    #Executando o config.py e analizando
        analyze_conditions()                     #Se as configs existem

        import pyfiglet                          #Coisas para deixar o terminal da maid bonito (eu n vou fazer uma gui pra ela)
        pyfiglet.print_figlet("Neko")            #Escreve "maid" de uma forma muito foda
        print("Programado por: Polarfill (https://github.com/PolarFill)")

        from MaidUtils.init import update
        update.Check()                           #Checa updates, e mostra se tiver algum mostra no terminal

        print("#####################################################" + Fore.CYAN)
        #print(Fore.CYAN + "Carregando a maid...")
        
        from MaidUtils.init import check_connection    #Checando se há uma conexão com a internet
        check_connection.Connection()
        
        from MaidUtils.init import initcheck           
        initcheck.Init()                               #Checa algumas configurações principais
        
    except Exception as x:
            from MaidUtils.init import crash_handler #Importando crash handler
            crash_handler.Handle(x, 'Inicialização') #Executando
        
    eternal_input()                                #Usuario é jogado para a função que analisa inputs, onde a magica acontece.  