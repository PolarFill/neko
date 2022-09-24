import configparser
from config import path
config = configparser.ConfigParser()

config.read([f'{path}/Userdata/Configurações/Reconhecimento_de_voz.ini', 
             f'{path}/Userdata/Maid/Session/session.info',
             f'{path}/Userdata/Configurações/Principal.ini'])
microfone = config.getint('STT', 'microfone')
auto_check = config.get('STT', 'auto-adjust')           
engine2 = config.get('STT', 'engine').lower()
timeout = config.getint('STT', 'timeout')
lang = config.get('STT', 'linguagem')
treshold = config.get('STT', 'fim-da-frase')
sensibilidade = config.get('STT', 'sensibilidade')
check = config.get('Geral', 'voice').lower()

if auto_check != 'auto':
    auto_check = float(auto_check)

from colorama import Fore, init
init()

def capture():    #Função responsavel por capturar input
    if check == 'false': #Se o controle por voz tiver desativado
        output = input(Fore.BLUE + "Input >> " + Fore.CYAN)
        print(Fore.RESET, end='\r')
        return output
    
    else: 
        import speech_recognition as sr
        r = sr.Recognizer()

        print(Fore.RED + "\033[KPegando dispositivo...", end='\r')
        if microfone == 1:                                #Pegando microfone definido pelo usuarío nas configs
            mic = sr.Microphone()                         #Caso o mic n seja 1 (principal), vai usar o definido pelo usuario
        else:
            mic = sr.Microphone(device_index=microfone)  

        print(Fore.YELLOW + "\033[KAjustando sensibilidade...", end='\r')
        with mic as source:
            if auto_check != '0':                      #Detectando a sensibilidade do mic
                if auto_check == 'auto':               
                    r.adjust_for_ambient_noise(source)    #Caso esteja como auto, a sensibilididade sera ajustada
                else:
                    r.adjust_for_ambient_noise(source, duration=auto_check)
            
            if treshold != 'false':
                float(treshold)
                r.pause_threshold(treshold)
            
            if sensibilidade.isdigit() and auto_check == '0':
                float(sensibilidade)
                r.energy_threshold(sensibilidade)
            
            print(Fore.GREEN + "\033[KCaptando audio!", end='\r')
            if timeout != 0 and timeout > 0:              #Checando se o usuario definiou um timeout
                audio = r.listen(source, phrase_time_limit=timeout)
            else:
                audio = r.listen(source)

        if audio == None:
            print(Fore.RED + "\033[KNada foi dito." + Fore.RESET)
        else:
            print(Fore.CYAN + "\033[KReconhecendo audio...", end='\r')

        try:
            if engine2 == 'google':     #Engines e keys da api da google (não confundir com google cloud)
                output = r.recognize_google(audio, key='AIzaSyAOC9oUf5AjOweXeEOowokEye6VRPx8cZo', language=lang)
            elif engine2 == 'wit':      #Engines e keys da api da wit
                if 'en' in lang:
                    output = r.recognize_wit(audio, key='IUIX2CGM5KIJDU43PR5B3SL5PGZQHZCL')    #key de reconhecimento em ingles
                else:
                    output = r.recognize_wit(audio, key='AAAK2MMLZVTDXRRCCZLMLLSPVFREAVRE')    #key em pt (padrão)
            elif engine2 == 'houndify': #Engine e keys da api do houndify (somente em inglês)
                output = r.recognize_houndify(audio, '1zxR5CQLcN8WkeasdtPIIg==', 
                                              'DPJHPtaNPq-xEk5rAepgA6wRwGMKEeRQmgr2ea0pBw9Ch8VMHOUESKjQF1kq9Ks2jiUd9rmDWOw7gSEmYdzyBQ==')
            elif engine2 == 'ibm':
                output = r.recognize_ibm(audio, '862b69d0-e889-45ce-b2fb-3884f043e7fc', 'OD_THRBibWIKhUOcVMn499bkLHnjNmKXCdyZykRAEwrn',
                                         language=lang)
            else:
                output = output = r.recognize_google(audio, key='AIzaSyAOC9oUf5AjOweXeEOowokEye6VRPx8cZo', language=lang) #por padrão, usa key da google
            output.lower()  #coloca o output em minusculo

            print(Fore.BLUE + "\033[KInput >>" + Fore.CYAN + f" {output}" + Fore.RESET)
            return output
        except ValueError: #essa exceção é levantada caso o usuarío não diga nada
            print(Fore.RED + "\033[KNada foi dito." + Fore.RESET)
            pass
        except sr.UnknownValueError: #não lembro quando essa exceção é levantada (top 10 programadores)
            print(Fore.RED + "\033[KNada foi dito." + Fore.RESET)
            pass
        except sr.RequestError:
            print(Fore.RED + "Um erro ocorreu durante o reconhecimento de fala.")
            print("Tente trocar a engine de reconhecimento de voz e tente novamente." + Fore.RESET)