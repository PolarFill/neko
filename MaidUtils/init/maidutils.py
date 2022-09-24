def Main(): #Função que inicializa o maidutils
    from MaidUtils.init.tts import say          #Importando função do tts
    from MaidUtils.init.voice import capture    #Importando função de captura de fala
    import subprocess
    import os
    from config import path
    
    
    if os.path.isfile(f'{path}/Userdata/Maid/MaidUtils/main.exe') == False:                         #Se nenhuma instalação da maidutils existir
        print('Nenhuma instalação da MaidUtils foi encontrada. Deseja instalar? (Y/N)')    #Pergunta se o usuario quer instalar ela
        esc = capture()                                                                                 
        if esc.lower() != 'y': return                                                               #Se não quiser, encerra a função
        
        say('Instalando MaidUtils...')
        if os.path.isdir(f'{path}/Userdata/Maid/MaidUtils') == False:                               #Se o diretório da maidutils não existir
            os.mkdir(f'{path}/Userdata/Maid/MaidUtils')                                             #Cria o diretório pra maidutils
        
        import requests, zipfile
        request = requests.get('https://github.com/PolarFill/MaidUtils/releases/download/v1.0/win-maidutils-v1.0.zip') #Pega o .zip dela do github
        with open(f'{path}/Userdata/Maid/MaidUtils/maidutils.zip', 'wb') as f:                      #Começa a escrever o zip
            f.write(request.content)    
        with zipfile.ZipFile(f'{path}/Userdata/Maid/MaidUtils/maidutils.zip', 'r') as zip:          #Abre o zip para começar a extração
            zip.extractall(f'{path}/Userdata/Maid/MaidUtils')
        os.remove(f'{path}/Userdata/Maid/MaidUtils/maidutils.zip')                                  #Remove o zip após extração
        
        say('Instalação concluída!')                                                                #Anuncia que a instalação foi concluida
    else:
        p1 = subprocess.Popen(f'{path}/Userdata/Maid/MaidUtils/main.exe', shell=True)
        p1.wait()
        
def Recheck(): #Checa por novos módulos instalados e desinstalados
    from MaidUtils.init.tts import say          #Importando função do tts
    import configparser
    import os
    from config import path
    
    config = configparser.ConfigParser()
    config.read(f'{path}/Userdata/Configurações/Principal.ini')                 #Lendo config principal
    
    found_modules = []                                                          #Array usada para guardar os módulos achados
    modules = os.listdir(f'{path}/Userdata/Maid/Modules')                       #Pegando itens no diretório de módulos da maid
    for i in modules:
        if os.path.isdir(f'{path}/Userdata/Maid/Modules/{i}'):                  #Checa se o item é um diretório e taca na found_modules
            found_modules.append(i)                                             #(!!!COMPLEXIDADE DESNECESSARIA, REESCREVER DEPOIS!!!)
       
    prefix_method = config.get('Geral', 'custom-prefixes').lower()   
       
    if prefix_method == 'true':                                                     #Caso o user use prefixos custom
        config.read(f'{path}/Userdata/Configurações/Prefixos.ini')                  #Lê o prefixos.ini pra escrever os prefixos do módulo lá
        conf_directory = '/Configurações/Prefixos.ini'                              
    else:
        if os.path.isfile(f'{path}/Userdata/Maid/Session/prefixes1.bin') == False: #Caso o user use prefixos padrão
            with open(f'{path}/Userdata/Maid/Session/prefixes1.bin', 'w') as f:  #Cria um prefixes1.bin caso não exista e joga os prefixos do módulo lá
                f.write()
        config.read(f'{path}/Userdata/Maid/Session/prefixes1.bin')
        conf_directory = '/Maid/Session/prefixes1.bin'
        
        if config.has_section('Modules') == False:
            config.add_section('Modules')
    
    variable_names = []   
    for i in found_modules:                                                                 #Para cada módulo encontrado
        if os.path.isfile(f'{path}/Userdata/Maid/Modules/{i}/prefixes.txt'):                #Pega o prefixes.txt (arquivo que define prefixos) se tiver
            with open(f'{path}/Userdata/Maid/Modules/{i}/prefixes.txt', 'r') as f:
                leitura = f.readlines()
                     
                for i in leitura:
                    
                    if i != '\n':
                        if '=' in i:
                            variable_name, default_value = i.split('=', 1)        #Pega o nome e valor padrão do prefixo, caso o dev especificado
                        else:
                            variable_name = i
                            default_value = '[""]'                                        #Caso o contrarío, seta o valor padrão como uma array
                        variable_name = variable_name.replace(' ', '')
                        default_value = default_value.replace(' ', '', 1)
                        variable_names.append(variable_name)                              #Taca o nome do prefixo em uma array pra checar depois
                            
                        config['Modules'][f'{variable_name}'] = default_value             #Cria valor no arquivo
                        
                        with open(f'{path}/Userdata{conf_directory}', 'w') as f:          #Salva config
                            config.write(f)
                    
                        print(f'Módulo encontrado! Módulo = {i}')
    
        for key in config['Modules']:                                                          #Checa se algum módulo foi removido
            if key not in variable_names:                                                      #Caso o prefixo não esteja na lista de prefixos
                config.remove_option('Modules', key)                                           #Remove o prefixo dele
        with open(f'{path}/Userdata{conf_directory}', 'w') as f:                               #Salva config
            config.write(f)                                                                    
            
def Run(cmd, prefixes):
    from config import path
    import subprocess 
    
    package = [i for i in prefixes if cmd in i]
    name, package = package.split('=', '1')
    
    if os.path.isdir(f'{path}/Userdata/Maid/Modules/{name}'):
        subprocess.Popen(f'{path}/Userdata/Maid/Modules/{name}/main.exe')
    
    #Separar o nome do pacote e o nome do prefixo
    #Pegar o executavel na pasta com o mesmo nome do pacote
    #Executar (talvez mandando o prefixo)
    #FAZER UM CÓDIGO QUE FAZ ISSO