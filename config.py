import configparser
import os, sys, platform

path = os.path.dirname(os.path.realpath(__file__))
if platform.system().startswith('W'):
    path = path.replace('\\', '/')

def analyze_conditions():
    
    #Essa função analisa se os arquivos da maid estão presentes
    #Se não estiver, esta função irá chamar outras funções para gerar estes arquivos
    
    if os.path.isdir(f'{path}/Userdata') == False or os.path.isdir(f'{path}/Userdata/Configurações') == False:
        print("AVISO: Arquivos de configuração não foram encontrados!")
        print("Gerando arquivos...")
        if os.path.isdir(f'{path}/Userdata') == False: #Se a userdata não existir, cria os arquivos da maid e etc
            mkconf_userdata()
        else:
            os.mkdir(f'{path}/Userdata/Configurações') #Se for só a pasta de config, cria só o configurações e etc
        mkconf_main()
        mkconf_voz()
        mkconf_tts()
        mkconf_custom()
        print("Arquivos de configuração gerados com sucesso!")
        print(f"Acesse as configurações pelo diretório \"{path}/Userdata/Configurações\"")
        print("Reinicie a maid para poder utiliza-lá.")
        input('(Pressione qualquer tecla para reiniciar a maid...)')
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        if os.path.isfile(f'{path}/Userdata/Configurações/Principal.ini') == False:
            mkconf_main()
        if os.path.isfile(f'{path}/Userdata/Configurações/Reconhecimento_de_voz.ini') == False:
            mkconf_voz()
        if os.path.isfile(f'{path}/Userdata/Configurações/TTS.ini') == False:
            mkconf_tts()
        if os.path.isfile(f'{path}/Userdata/Configurações/Customizações.ini') == False:
            mkconf_custom()
        if os.path.isfile(f'{path}/Userdata/Configurações/Prefixes.ini') == False:
            mkconf_prefixes()
                           
    if os.path.isfile(f'{path}/Userdata/Maid/Session/session.info') == True:
        os.remove(f'{path}/Userdata/Maid/Session/session.info')
        mkconf_session()
    else:
        mkconf_session()
    
##################################################################################################
#A seguir se encontram as funções responsaveis por
#Gerar as configurações
##################################################################################################

def mkconf_main():
    
    #Função usada para gerar a
    #Configuração principal
    
    config = configparser.ConfigParser(allow_no_value=True)
    config['Version'] = {
        '; NAO ALTERE ESTES VALORES.': None,
        '; ELES SAO UTILIZADOS PARA ATUALIZAR A MAID.': None,
        'version': 'v1.0',
        'target': 'v1.0',
        'type': 'normal-win-maid',
    }
    config['Geral'] = {
        '; Caso o valor esteja como "true", habilitara o terminal. Valor padrao: "true"': None,
        'mostrar-terminal': 'true',
        ' ': None,
        '; Caso o valor esteja como "false", desabilitara o TTS.':  None,
        '; Caso desabilite essa funcao juntamente com a funcao "mostrar-terminal", a maid nao funcionara.': None,
        '; Valor padrao: "true"': None,
        'tts': 'true',
        '    ': None,
        '; Caso o valor esteja como "false", desabilita o controle por voz da maid. Valor padrao: "true"': None,
        'voice': 'true',
        '  ': None,
        '; Caso o valor esteja como "true", iniciara a maid como administrador/root. Valor padrao: "false"': None,
        'admin': 'false',
        '   ': None,
        '; Caso o valor esteja como "true", a maid ficara completamente offline. Valor padrao: "false"': None,
        'modo-offline': 'false',
        '     ': None,
        '; Define a frase utilizada para ativar a maid. Valor padrao: "ok maid"': None,
        'prefixo': 'executar',
        '      ': None,
        '; Caso o valor esteja como "false", o prefixo nao sera utilizado. Valor padrao: "true"': None,
        'usar-prefixo': 'true',
        '        ': None,
        '; Caso o valor esteja como "false", a checagem automatica de updates sera desativada. Valor padrao: "true"': None,
        'checar-updates': 'true',
        '       ': None,
        '; Caso o valor esteja como "true", e o valor de "checar-updates" tambem estiver em "true"': None,
        '; O update sera baixado automaticamente': None,
        'baixar-updates': 'false',
        '         ': None,
        '; Se o seu sistema for windows, a opcao "quickedit" pode vir ligada por padrao, e isso pode travar a maid.': None,
        '; Caso o valor esteja como "true", essa opcao sera desativada apenas para o terminal da maid, eliminando travamentos,': None,
        '; porem a opcao de copiar e colar nao estara mais disponivel. Valor padrao: "true"': None,
        'patch-quickedit': 'false',
        '          ': None,
        '; Caso a configuracao abaixo esteja como "true", toca uma musica de fundo enquanto a maid estiver aberta.': None,
        '; Defina o diretorio da musica no "background-music-path", e o volume no "background-music-volume".': None,
        '; Defina quantas vezes a musica deve tocar no "background-music-loop". Deixe o valor como "-1" para um loop': None,
        '; Formatos suportados: mp3, ogg, wav': None,
        'background-music': 'false',
        'background-music-path': '',
        'background-music-volume': '',
        'background-music-loop': '-1',
        '           ': None,
        '; Caso o valor seja "true", usa uma lista customizada de gatilhos para os comandos da maid.': None,
        '; A performance, porem, pode ser afetada. Valor padrao: "false".': None,
        'custom-prefixes': 'false',
        '            ': None
    }
    config['MaidUtils'] = {
        '; Caso o valor seja "false", desativa a MaidUtils. Valor padrao: "true"': None,
        'maidutils': 'True',
        '             ': None,
        '; Caso o valor seja "false", desativa os modulos da maidutils, deixando apenas os modulos padroes. Valor padrao: "true"': None,
        'modules': 'false'
    }
    with open(f'{path}/Userdata/Configurações/Principal.ini', 'w') as configfile1:
        config.write(configfile1)    

def mkconf_voz():
    
    #Função usada para gerar a
    #Configuração de voz

    config = configparser.ConfigParser(allow_no_value=True)
    
    config['STT'] = {
    '; Aviso: estas opcoes surtirao efeito apenas se o reconhecimento de voz estiver habilitado': None,
    '': None,
    '; Ajusta a sensibilidade do microfone automaticamente': None,
    '; Deixe o valor como "0" para desativar esta funcao.': None,
    '; Deixe como "auto" para detectar um valor ideal automaticamente.': None,
    '; Deixe o valor como qualquer outro numero para definir o maximo de tempo que a maid pode ajustar a sensibilidade.': None,
    '; Valor padrao: "auto"': None,
    'auto-adjust': 'auto',
    ' ': None,
    '; Define a sensibilidade do microfone manualmente.': None,
    '; Caso o valor esteja como "false", a sensibilidade ira ser ajustada automaticamente.': None,
    '; Valor padrao: "false"': None,
    'sensibilidade': 'false',
    '     ': None,
    '; Define a engine que sera utilizada para reconhecimento de voz. Caso a maid esteja em modo offline, sera utilizado sphinx': None,
    '; Engines validas: "sphinx", "google", "ibm", "wit", "houndify"': None,
    '; Valor padrao: "google"': None,
    'engine': 'google',
    '  ': None,
    '; Define o microfone que sera utilizado para reconhecimento de voz. Mude este numero caso queira utilizar outro microfone': None,
    '; Valor padrao: "1"': None,
    'microfone': '1',
    '   ': None,
    '; Define a quantidade de tempo que a maid ira esperar para processar a frase dita.': None,
    '; Caso o valor seja "0", a maid nao ira funcionar.': None,
    '; Caso o valor "auto-adjust" esteja ativado, o timeout nao ira funcionar.': None,
    '; Valor padrao: "2"': None,
    'timeout': '2',
    '    ': None,
    '; Define quanto tempo de silencio e necessario para uma frase ser reconhecida como terminada.': None,
    '; Caso o valor seja "false", a opcao padrao sera utilizada. Valor padrao: "false"': None,
    'fim-da-frase': 'false',
    '      ': None,
    '; Define em que linguagem a voz sera interpretada. Usado por algumas engines. Valor padrao: "pt-br"': None,
    'linguagem': 'pt-br'
    }
    with open(f'{path}/Userdata/Configurações/Reconhecimento_de_voz.ini', 'w') as configfile2:
        config.write(configfile2)
        
def mkconf_tts():
    
    #Função usada para gerar a
    #Configuração de TTS

    config = configparser.ConfigParser(allow_no_value=True)
    
    config['TTS'] = {
    '; AVISO: ESTAS OPCOES APENAS SURTIRAO EFEITO SE O TTS ESTIVER HABILITADO': None,
    '': None,
    '; Define a engine que sera utilizada para fala. Valor padrao: "gtts"': None,
    '; Engines disponiveis: gtts, ttsx3, watson': None,
    'tts-engine': 'gtts',
    }
    config['TTSX3'] = {
    '; AVISO: ESTAS OPCOES APENAS SURTIRAO EFEITO SE A ENGINE DO TTS FOR "TTSX3"': None,
    '; Define a engine que sera utilizada no ttsx3. Valor padrao: "sapi5"': None,
    '; Engines disponiveis: espeak, sapi5, nsss': None,
    'engine': 'sapi5',
    '    ': None,
    '; Muda a voz sendo utilizada no pyttsx3.': None, 
    '; Caso queira usar uma outra voz instalada no sistema, mude este numero de 1 em 1.': None,
    '; Valor padrao: "1"': None,
    "id": '1',
    '       ': None,
    '; Insira o volume da voz desejado abaixo (Minimo = 0, Maximo = 1). Valor padrao: "0.5"': None,
    'volume': '0.5',
    }
    config['GTTS'] = {
    '; Define a linguagem utilizada. Valor padrao: "pt"': None,
    'linguagem': 'pt',
    '     ': None,
    '; Define o tld da api TTS da google (raramente precisa ser mudado). Valor padrao: "com.br"': None,
    'tld': 'com.br',
    }
    config['WATSON'] = {
    '; Define a voz que sera utilizada. Para uma lista de vozes disponiveis, acesse o link abaixo.': None,
    '; https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-voices': None,
    '; Valor padrao: pt-BR_IsabelaV3Voice': None,
    'watson-voice': 'pt-BR_IsabelaV3Voice',
    '        ': None,
    '; Define o formato em que o audio sera salvo. Valor padrao: "mp3"': None,
    '; Formatos disponiveis: mp3, wav, ogg': None,
    'watson-format': 'mp3'
    }
    with open(f'{path}/Userdata/Configurações/TTS.ini', 'w') as configfile3:
        config.write(configfile3)

def mkconf_custom():
    
    #Função usada para gerar o arquivo
    #que irá conter a maioria das customizações da maid
    
    config = configparser.ConfigParser(allow_no_value=True)

    config["Custom"] = {
    '; Muda o nome da maid na maior parte das referencias a ela.': None,
    'name': 'maid',
    '': None,
    '; Muda o titulo da janela da maid.': None,
    'title': 'Maid',
    ' ': None
    }

    with open(f'{path}/Userdata/Configurações/Customizações.ini', 'w') as file: 
        config.write(file)
    

def mkconf_session(): 

    #Função usada para gerar o arquivo
    #que irá conter as informações da sessão
    
    config = configparser.ConfigParser(allow_no_value=True)

    config["Session"] = {
    "online": '', 
    "tts": '',
    'google': '',
    "mic-output": '',
    'tempnote': '',
    'spotify': '',
    'youtube': '',
    'playlist': '',
    }

    with open(f'{path}/Userdata/Maid/Session/session.info', 'w') as file: 
        config.write(file)
 
def mkconf_userdata():
    
    #Função usada para gerar
    #A userdata
    
    os.mkdir(f'{path}/Userdata')
    os.mkdir(f'{path}/Userdata/Maid')
    os.mkdir(f'{path}/Userdata/Maid/Session')
    os.mkdir(f'{path}/Userdata/Maid/Tools')
    os.mkdir(f'{path}/Userdata/Configurações')
    os.mkdir(f'{path}/Userdata/Userspace')
    
def mkconf_prefixes():
    
    #Função usada para gerar a
    #Configuração dos prefixos (caso esteja configurado para isso)
    
    config0 = configparser.ConfigParser(allow_no_value=True)
    config0.read(f'{path}/Userdata/Configurações/Principal.ini')         #Lê o arquivo principal
    if config0.get('Geral', 'custom-prefixes').lower() == 'true':        #Se custom-prefixes estiver true
        if os.path.isfile(f'{path}/Userdata/Configurações/Prefixos.ini') == True: #Checa se o arquivo existe
            pass
        else:
            config0['Ajuda'] = {
                '; Para adicionar prefixos customizados, basta ir nos prefixos da acao e adicionar um prefixo.': None,
                '; E possivel adicionar varios prefixos para uma acao, porem, nesse caso e necessario adicionar uma virgula e aspas': None,
                '; para cada prefixo. Caso tenha duvidas, siga o exemplo abaixo:': None,
                '; wikipedia = ["wikipedia", "pesquisar wikipedia", "wiki"]': None,
                '; Para adicionar apenas um prefixo para uma acao, apenas coloque o prefixo no meio das aspas, como no exemplo abaixo:': None,
                '; wikipedia = ["wikipedia"]': None
            }
            config0['Prefixos'] = {
                'prefixo-cancelar': '[""]',
                'prefixo-tempo': '[""]',
                'prefixo-data': '[""]',
                'prefixo-dado': '[""]',
                'prefixo-fala': '[""]',
                'prefixo-print': '[""]',
                'prefixo-sair': '[""]',
                'prefixo-reiniciar': '[""]',
                'prefixo-nota-temporaria': '[""]',
                'prefixo-ler-nota-temporaria': '[""]',
                'prefixo-speedtest': '[""]',
                'prefixo-controle-janela': '[""]',
                'prefixo-desligar-pc': '[""]',
                'prefixo-joquempo': '[""]',
                'prefixo-volume': '[""]',
                'prefixo-wikipedia': '[""]',
                'prefixo-playlist-local': '[""]',
                'prefixo-parar-musica': '[""]',
                'prefixo-temporizador': '[""]',
                'prefixo-cronômetro': '[""]',
                'prefixo-changelog': '[""]',
                'prefixo-inicializar-maidutils': '[""]',
            }
            with open(f'{path}/Userdata/Configurações/Prefixos.ini', 'w') as configfile4:
                config0.write(configfile4)