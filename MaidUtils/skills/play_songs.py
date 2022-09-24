import queue
yt_fifo = queue.Queue(maxsize=1000)
from colorama import Fore, init
init()

def LocalPlay(command): #Toca musícas de uma playlist local
    from MaidUtils.init.tts import say          #Importando função do tts
    from config import path
    from commands import answers_local_playlist
    import configparser
    import contextlib                           #Só pra importar o pygame sem mensagemKKKKKKKKKK
    import platform
    import os
    
    import configparser
    from config import path
    
    config = configparser.ConfigParser()
    config.read(f'{path}/Userdata/Maid/Session/session.info') #Lendo arquivo de sessão
    config.set('Session', 'playlist', 'True')
    with open(f'{path}/Userdata/Maid/Session/session.info', 'w') as configfile:
            config.write(configfile)
    
    if command in answers_local_playlist:           #Se o comando for só "playlist" e etc
        say("\nSelecione o diretório da playlist")
        from tkinter import filedialog, Tk          #Função do tkinter pra escolher diretório
        root = Tk()                                 #Configurando tkinter...
        root.withdraw()
        audiopath = filedialog.askdirectory()       #Executando dialogo
        if platform.system().startswith('W'):
            audiopath = audiopath.replace('\\', '/')
    else:                                           #Se o comando tiver um argumento (diretório) nele
        for i in answers_local_playlist:            #Checa array com respostas da playlist
            command = command.replace(i, '', 1)     #Remove essas respostas do input pra usar ele como diretório
        audiopath = command.lstrip()                #Remove espaço no começo do comando
    
    say("Aguarde...")
    
    musics = []  #Array onde os diretórios das musícas serão guardados
    
    for i in os.listdir(audiopath): #Para cada arquivo no diretório fornecido
        if i.endswith(('.mp3', '.ogg', '.wav')): #Se o arquivo termina em mp3, ogg, ou wav
            song = ''.join([f'{audiopath}', '/', f'{i}']) #Bota na array
            musics.append(song)
    
    if not musics: #Se a array de musicas estiver vazia (nenhuma musica foi encontrada)
        say(Fore.RED + "\nNenhuma musíca compatível foi encontrada no diretório" + Fore.RESET)
    
    with contextlib.redirect_stdout(None): #Importa o pygame com o stdout redirecionado para None
        import pygame                      #Para ele não mostrar a mensagem de import no terminal
        pygame.init()                                                #Iniciando pygame 
        pygame.mixer.init()                                          #Iniciando mixer
        
    for i in musics:
        try:
            song_name = os.path.basename(os.path.normpath(i)) #Extraindo nome da musica
            print(Fore.BLUE + f"Tocando {song_name}..." + Fore.RESET)
            pygame.mixer.music.load(i)                                   #Carregando musica
            pygame.mixer.music.play()                                    #Tocando audio
            while pygame.mixer.music.get_busy():                         #Espera o audio tocar para destruir o objeto
                pygame.time.Clock().tick(10)                             #Esperando...
            pygame.mixer.music.unload()                                  #Descarregando arquivo
        except pygame.error: #Se o playback da musica falhar
            print(Fore.RED + f"Um erro ocorreu enquanto a maid tocava {song_name}.") #Anuncia erro
            if song_name.endswith('.ogg'):
                print("Certifique-se que o ogg utilize o codec \"Vorbis\".") #Aviso que pode ser o codec caso seja ogg
            print("Pulando musíca..." + Fore.RESET)
            continue #Pula musica
        
        pygame.mixer.music.stop() #Encerrando mixer, após todas as musícas tocarem

#############################
#########FUNÇÃO DO YOUTUBEKKKKKKKKKKK
#############################

def Youtube(search, setlink=None, debugmode=None): #Converte o audio do youtube para pcm e toca em tempo real (usa ffmpeg)
    import platform #Importa o platform para analizar a plataforma
    import contextlib #Importa o pygame sem a mensagemKKKKKK
    import configparser #Seta no session.info que uma musica está tocando
    import youtube_dl #Importa ytdl pra pegar info do vídeo
    import subprocess #Usado para dar o comando do ffmpeg
    import numpy #Usado para guardar o pcm
    from threading import Thread
    import sounddevice as sd #Usado para tocar a musíca
    
    if debugmode == None:
        from config import path #Importa o path do config.py
    else:
        path = os.path.dirname(os.path.realpath(__file__))
        if platform.system().startswith('W'):
            path = path.replace('\\', '/')
    
    config = configparser.ConfigParser()                                        #Executa configparser
    config.read(f'{path}/Userdata/Maid/Session/session.info')                   #Lê o arquivo de sessão
    config.set('Session', 'youtube', 'True')                                    #Indica que uma musica esta tocando
    with open(f'{path}/Userdata/Maid/Session/session.info', 'w') as configfile: #Escreve mudanças para o arquivo
        config.write(configfile)    
    
    if setlink != None: #Se o setlink for None (indica que nenhum link foi fornecido)
        from pytube import Search #Importa livraria para pesquisar no youtube
        link = Search(search)
    else: #Caso o contrario
        link = search #O link será o search (link inserido pelo usuario)
    
    with contextlib.redirect_stdout(None): #Redirecionando output para none
        with youtube_dl.YoutubeDL() as ydl: #Iniciando youtube-dl
            song_info = ydl.extract_info(link, download=False) #Extrai info do vídeo
    song_link = song_info["formats"][0]["url"] #Link do audío do vídeo 
    
    if Check_ffmpeg() == 'path':                                   #Se o user tiver ffmpeg
        ffmpeg_start = 'ffmpeg'                                    #Usa ffmpeg normal
    else:
        ffmpeg_start = f'{path}/Userdata/Maid/Tools/ffmpeg.exe'    #Se não tiver usa o ffmpeg da maid
         
    Thread(target=Youtube_ffmpeg_thread, args=(ffmpeg_start, song_link)).start() #Inicia a thread onde o ffmpeg converte o audio
    while yt_fifo != '':
        data = numpy.frombuffer(yt_fifo.get(), numpy.float32).reshape([-1, 2])
        sd.play(data=data, samplerate=44100)
        #stream.write(data)
        
    
def Youtube_ffmpeg_thread(start, link):
    import subprocess
    
    ffmpeg_process = subprocess.Popen('{} -i "{}" -f f32le -loglevel quiet -acodec pcm_f32le -ar 44100 -ac 2 -'.format(start, link), 
                     stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=10**8) #Comando que converte audio do video para pcm
    output = ffmpeg_process.stdout.read(352800) #Lê 51k de bytes do subprocesso #dtype 51200 #dtype 352.800 #dtype 256000
    yt_fifo.put(output)  #Coloca esses bytes no queue setado no module level
    print('queue botado e etc')
    while output: #Repete😎
        print('')
        output = ffmpeg_process.stdout.read(352800)
        yt_fifo.put(output) 
    

def Youtube2(search, setlink=None): #Pega musicas e etc do youtube (utilizado caso o usuario não tenha ffmpeg)
    import platform #Importa o platform para analizar a plataforma
    import contextlib #Importa o pygame sem a mensagemKKKKKK
    import configparser #Seta no session.info que uma musica está tocando
    import youtube_dl #Importa ytdl pra pegar o mp3/ogg
    from config import path #Importa o path do config.py
    with contextlib.redirect_stdout(None): #Importa o pygame com o stdout redirecionado para None
        import pygame                      #Para ele não mostrar a mensagem de import no terminal
    
    audiopath = f"{path}/Userdata/Maid/Session/tempytb.mp3"   #O diretório do audio será composto de /
    
    args = {'format': 'mp3',                   #Define que o audio em mp3 será baixado
            'noplaylist': 'True',              #Define que playlists não serão baixadas
            'outtmpl': f'{audiopath}'}         #Define o nome do arquivo da musica
    
    if setlink != None: #Se o setlink for None (indica que nenhum link foi fornecido)
        from pytube import Search #Importa livraria para pesquisar no youtube
        s = Search(search)
        print(s)
        
    else: #Caso o contrario
        link = search #O link será o search (link inserido pelo usuario)
    
    config = configparser.ConfigParser()                                        #Executa configparser
    config.read(f'{path}/Userdata/Maid/Session/session.info')                   #Lê o arquivo de sessão
    config.set('Session', 'youtube', 'True')                                    #Indica que uma musica esta tocando
    with open(f'{path}/Userdata/Maid/Session/session.info', 'w') as configfile: #Escreve mudanças para o arquivo
        config.write(configfile)
    
    try:
        with youtube_dl.YoutubeDL(args) as ydl: #Iniciando youtube-dl
            ydl.download([f'{search}'])         #Baixando arquivo em mp3
    except youtube_dl.utils.DownloadError:
        
        try:
            args = {'format': 'ogg',                   #Define que o audio em ogg será pego
                    'noplaylist': 'True',              #Define que playlists não serão baixadas
                    'outtmpl': f'{audiopath}'}         #Define o nome do arquivo da musica
            
            with youtube_dl.YoutubeDL(args) as ydl: #Iniciando youtube-dl
                ydl.download([f'{search}'])         #Baixando arquivo em ogg
        except:
            from colorama import init, Fore; init()
            print(Fore.RED + "Um erro ocorreu durante a reprodução do audío")
            print("Tente instalar ffmpeg para maior compatibilidade e mais velocidade" + Fore.RESET)
            
      
    pygame.init()                                                #Iniciando pygame 
    pygame.mixer.init()                                          #Iniciando mixer
    pygame.mixer.music.load(audiopath)                           #Carregando musica
    pygame.mixer.music.play()                                    #Tocando audio
    while pygame.mixer.music.get_busy():                         #Espera o audio tocar para destruir o objeto
        pygame.time.Clock().tick(10)                             #Esperando...
    pygame.mixer.music.unload()                                  #Descarregando arquivo
    pygame.mixer.music.stop()                                    #Encerrando mixer

    os.remove(audiopath)                                         #Remove audio
        
    config.read(f'{path}/Userdata/Maid/Session/session.info')
    config.set('Session', 'youtube', 'False')
    with open(f'{path}/Userdata/Maid/Session/session.info', 'w') as configfile:
        config.write(configfile)
    
#############################
#########FUNÇÃO DE CHECAGEM
#############################

def Check_ffmpeg(): #Checa se o usuario tem ffmpeg
    import subprocess
    from config import path
    try:
        command = subprocess.check_output('ffmpeg -h', shell=True, encoding='utf8', stderr=subprocess.PIPE) #Dá o comando de help do ffmpeg
        return 'path' #Se o comando retornar 0, o comando deu certo e o ffmpeg está instalado
    except subprocess.CalledProcessError:         #Caso o contrario
        from config import path                   #Se não estiver, checa a instalação da maid
        import os
        if os.path.isfile(f'{path}/Userdata/Maid/Tools/ffmpeg.exe') == True: #Se o ffmpeg.exe na pasta da maid existir
            return 'base'   #Indica que existe uma instalação do ffmpeg da maid
        else:
            return False    #Indica que não tem ffmpeg nesse pc

def Install_ffmpeg(): #Instala ffmpeg
    import os
    import shutil   #Usado para mover o ffmpeg
    import requests #Usado para baixar o ffmpeg
    import py7zr    #Usado para descompactar
    #from colorama import init, Fore #Só pra deixar bonito mesmo
    from config import path
    #init()

    #print(Fore.BLUE + 'Baixando ffmpeg...' + Fore.RESET)
    request = requests.get('https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z') #Pega conteudo do bin do ffmpeg 
    with open(f'{path}/Userdata/Maid/Tools/temp-ffmpeg.7z', 'wb') as zipfile:             #E escreve em um 7z
        zipfile.write(request.content)
        
    #print(Fore.Blue + "Descompactando ffmpeg..." + Fore.RESET)                      
    with py7zr.SevenZipFile(f'{path}/Userdata/Maid/Tools/temp-ffmpeg.7z', 'r') as zipfile:   #Descompacta o 7z do ffmpeg
        zipfile.extractall(path=f'{path}/Userdata/Maid/Tools/extracted')

    print("foda")
    #print(Fore.BLUE + "Ajustando instalação..." + Fore.RESET)
    

def Check(): #Checa se alguma musica está tocando
    import configparser
    from config import path
    
    config = configparser.ConfigParser()
    config.read(f'{path}/Userdata/Maid/Session/session.info') #Lendo arquivo de sessão
    
    if config.get('Session', 'spotify') == 'True': #Checando se spotify está tocando
        
        config.set('Session', 'spotify', 'False') #Se tiver, muda o valor de tocando pra inativo
        with open(f'{path}/Userdata/Maid/Session/session.info', 'w') as configfile:
            config.write(configfile)
            
        return 'spotify' #Retorna que o spotify está ativo para assim matar o processo dele
    
    elif config.get('Session', 'youtube') == 'True': #checa se o youtube está tocando
        
        config.set('Session', 'youtube', 'False') #Se tiver, muda o valor de tocando pra inativo
        with open(f'{path}/Userdata/Maid/Session/session.info', 'w') as configfile:
            config.write(configfile)
            
        return 'youtube' #Retorna que o youtube está ativo para assim matar o processo dele
    
    elif config.get('Session', 'playlist') == 'True':
        
        config.set('Session', 'playlist', 'False')
        with open(f'{path}/Userdata/Maid/Session/session.info', 'w') as configfile:
            config.write(configfile)
            
            return 'LocalPlaylist'
        
    else:
        return 0
    
if __name__ == '__main__':
    cmd = input()
    Youtube(cmd)