import configparser
import re
from config import path

config = configparser.ConfigParser()
config.read([f"{path}/Userdata/Configurações/Principal.ini", 
                f"{path}/Userdata/Maid/Session/session.info", 
                f"{path}/Userdata/Configurações/TTS.ini"])

def remove_esc(text): #Remove escape codes da string, caso a maid for falar ela
    remove_ansi = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])') 
    remove_ansi.sub('', text) #Remove os escapes codes
    return text #Retorna o texto sem eles
    
#########################################################

def pytts(text): #Função responsavel pela fala do pyttsx3
    import pyttsx3

    engine = config.get('TTSX3', 'engine')
    volume = config.get('TTSX3', 'volume')
    gender = config.getint('TTSX3', 'id') #Esta é a id da voz, não o gênero. Não mude o nome da variavel, risco de quebra de código.
    
    if engine != 'sapi5' or engine != 'nsss' or engine != 'espeak':     #Checa se a engine definida é valida
        engine = 'sapi5'                                                #Se não for, define a engine como sapi5
    
    if volume < '0' or volume > '1': #Checa se o volume definido é menor que 0 ou maior que 1
        volume = '0.5'               #Se for, coloca o volume em 0.5

    engine = pyttsx3.init(driverName=engine)
    engine.setProperty('volume', volume)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[gender].id)

    engine.say(text)
    engine.runAndWait()

#########################################################

def google(text): #Função responsavel pela fala do gTTS
    import gtts, os
    import contextlib
    
    with contextlib.redirect_stdout(None): #Importa o pygame com o stdout redirecionado para None
        import pygame                      #Para ele não mostrar a mensagem de import no terminal

    localized = ['en', 'fr', 'zh-CN', 'zh-TW', 'pt', 'es']      #Lista de linguagens contendo locales
    linguagem = config.get('GTTS', 'linguagem')                 #Pegando linguagem preferida
    tld = config.get('GTTS', 'tld')                             #Pega o tld (subdominio, tipo com.br)

    mp3_path = f"{path}/Userdata/Maid/Session/tempfile.mp3"    #O diretório do mp3 será composto de /

    try:
        if linguagem in localized:                                  #Checando se a linguagem tem algum locale
            audio = gtts.gTTS(lang=linguagem, tld=tld, text=text)
        else:                           
            audio = gtts.gTTS(lang=linguagem, text=text)

        audio.save(mp3_path)  #Salvando output do gtts em um arquivo temporario
        
                                                                     #Abrindo arquivo
        pygame.init()                                                #Iniciando pygame 
        pygame.mixer.init()                                          #Iniciando mixer
        pygame.mixer.music.load(mp3_path)                            #Carregando musica
        pygame.mixer.music.play()                                    #Tocando audio
        while pygame.mixer.music.get_busy():                         #Espera o audio tocar para destruir o objeto
            pygame.time.Clock().tick(10)                             #Esperando...
        pygame.mixer.music.unload()                                  #Descarregando mp3
        pygame.mixer.music.stop()                                    #Encerrando mixer                              
        os.remove(mp3_path)                                          #Remove audio
    except AssertionError:
        pass

#########################################################

def watson(text): #Função responsavel pela fala do watson (ibm)
    import os, contextlib
    from ibm_watson import TextToSpeechV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    
    with contextlib.redirect_stdout(None): #Importa o pygame com o stdout redirecionado para None
        import pygame                      #Para ele não mostrar a mensagem de import no terminal
    
    formato = config.get('WATSON', 'watson-format').lower()
    voice = config.get('WATSON', 'watson-voice')
    
    key = 'MOWOYr8Oz4EnhaXOMcBLoPGg2OVMXDDfBMPcDND8YTio' #API key
    url = 'https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/12f6a6aa-60a8-4a0b-8cdf-19940fd70109' #Url pra requests

    audiopath = "{}/Userdata/Maid/Session/tempfile.{}".format(path, formato)
    
    auth = IAMAuthenticator(key)             #Autenticador para o tts
    tts = TextToSpeechV1(authenticator=auth) #Serviço tts
    tts.set_service_url(url)                 #Setando url q será usada para as requests
    
    with open(audiopath, 'wb') as audiofile:                          #Criando arquivo para escrita
        result = tts.synthesize(text, accept=f'audio/{formato}', voice=voice).get_result() #Mandando texto para criação do arquivo
        audiofile.write(result.content)                                                    #Escrevendo audio
        
    pygame.init()                                                #Iniciando pygame 
    pygame.mixer.init()                                          #Iniciando mixer
    pygame.mixer.music.load(audiopath)                           #Carregando musica
    pygame.mixer.music.play()                                    #Tocando audio
    while pygame.mixer.music.get_busy():                         #Espera o audio tocar para destruir o objeto
        pygame.time.Clock().tick(10)                             #Esperando...
    pygame.mixer.music.unload()                                  #Descarregando arquivo
    pygame.mixer.music.stop()                                    #Encerrando mixer                              
    os.remove(audiopath)                                         #Remove audio

#########################
###FUNÇÃO DE FALA
#########################

def say(text, out=None):  #Função responsavel pela fala, analisa a engine que o usuario prefere e passa o text para ela.
                          #Coloque o arg "out" em outro valor para não mostrar o output no terminal
    if out != None: 
        pass
    else:
        print(f"Output >> {text}") #Mostrando output no terminal
    
    if config.get('Geral', 'tts').lower() == 'false': #Checa se o usuarío desativou tts
        pass
    else:
        text = remove_esc(text=text)
        if (config.get('Session', 'online') == 'true'                          #Checa se o usuarío está offline
            and config.get('TTS', 'tts-engine').lower() == 'gtts'):            #ou prefere ttsx3     
            google(text=text)                                                  #executa a api da google
            
        elif (config.get('Session', 'online') == 'true'
            and config.get('TTS', 'tts-engine').lower() == 'watson'):
            watson(text=text)                                                  #executa o watson da ibm
        
        else:
            pytts(text=text)                                                   #executa pyttsx3