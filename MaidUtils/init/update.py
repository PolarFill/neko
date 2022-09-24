def Check(): #Checa por updates no repositório
    
    #COMO FUNCIONA AS VERSÕES:
    #1 parte - Define a plataforma da versão ("win" e "linux")
    #2 parte - Define se o bin é normal ou onefile ("normal" e "onefile")
    #3 parte - Só fala maid, n representa nada
    
    import configparser
    from config import path
    
    config = configparser.ConfigParser()
    config.read(f"{path}/Userdata/Configurações/Principal.ini")
    
    if config.get('Geral', 'checar-updates').lower() == 'true': #Checando se auto-checar atualizações está ativo
        import requests

        print("Checando atualizações...", end='\r')
        link = 'https://github.com/PolarFill/maid/releases/latest'


        response = requests.get('https://api.github.com/repos/PolarFill/maid/releases/latest') #Pagína das releases da maid no github
        version = response.json()["tag_name"]                                       #Pegando a tag
        
        if version == config.get('Version', 'version'):                      #Se a versão bater com a tag da ultima release
            print("\033[KNenhuma atualização foi encontrada!")                #Falar que não há atualizações
        else:                                                                #Caso o contrario
            if config.get('Geral', 'baixar-updates').lower() == 'false':     #Se auto-baixar updates estiver desativado
                print(f"\033[KAtualização encontrada! Para baixar, acesse {link}") #Só avisa que um update está disponivel
            else:
                print(f"\033[KUpdate encontrado! Baixando update...", end='\r')
                
                from config import path #importando path do config
                
                type_download = config.get('Version', 'type')
                
                link_download = 'https://github.com/PolarFill/maid/releases/download/' #Define o link de download base
                link_download_novo = link_download.join(['{}'.format(response.json()['tag_name']), f'{type_download}', '.zip'])
                #Junta a tag da versão q vai ser baixada + o tipo de download + .zip no link
                
                get_download = requests.get(link_download_novo)
                
                with open('{}/maid-{}.zip'.format(path, config.get('Version', 'version')), 'wb') as output:
                    output.write(get_download.content)
                
                print(f'\033[KUpdate baixado com sucesso no diretório {path}!')

def Changelog(command): #Pega o changelog da maid
    import configparser
    import requests
    import codecs, re
    from colorama import Fore, init
    from config import path
    from commands import answers_changelog
    init()
    
    config = configparser.ConfigParser()
    config.read(f"{path}/Userdata/Configurações/Principal.ini")
    
    if command in answers_changelog: #Se o changelog tiver na answers_changelog (significa pegar o changelog mais recente da maid)
        response = requests.get('https://api.github.com/repos/PolarFill/maid/releases/latest') #Pagína das releases da maid no github
        version = response.json()["tag_name"] #Pega versão da release para falar
        corpo = response.json()["body"] #Pegando a tag
        
    elif 'current' in command: #Se o changelog tiver current (significa pegar o changelog da versão atual da maid)
        response = requests.get('https://api.github.com/repos/PolarFill/maid/releases?per_page=100') #Pagína das releases da maid no github
        version = response.json()["tag_name"] #Pega versão da release para falar
        corpo = response.json()["body"] #Pegando a tag
            
    escape_sequences = re.compile(r'''
                                ( \\U........
                                | \\u....
                                | \\x..
                                | \\[0-7]{1,3}
                                | \\N\{[^}]+\}
                                | \\[\\'"abfnrtv]
                                )''', re.UNICODE | re.VERBOSE) 
    #Pega os escape codes. Para mais detalhes, leia https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python

    def decode_escapes(s):  #Função chamada para decodificar os escape codes
        def decode_match(match): #Função chamada para pegar o match
            return codecs.decode(match.group(0), 'unicode-escape') #Decodificando
        return escape_sequences.sub(decode_match, s) #Substituindo strings         
    
    print(Fore.BLUE + f"Changelog da maid {version}")
    print('')
    print(decode_escapes(corpo) + Fore.RESET)
    print('')
        
    
        
        
        