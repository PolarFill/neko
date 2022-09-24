import configparser, os
from config import path
config = configparser.ConfigParser()

if os.path.isfile(f'{path}/Userdata/Configurações/Principal.ini') == True:
    config.read(f'{path}/Userdata/Configurações/Principal.ini')

if config.get('Geral', 'custom-prefixes').lower() != 'true' or os.path.isfile(f'{path}/Userdata/Configurações/Prefixos.ini') == False:
    answers_cancelar = ['cancelar', 'nada', 'esquece', 'deixa']
    answers_hora = ['horas', 'hora', 'tempo']
    answers_data = ['data', 'dia', 'que dia é hoje']
    answers_dado = ['jogue um dado', 'joga um dado', 'jovem um dado', 'role um dado', 'dado']
    answers_say = ['diga', 'fale', 'funny', 'Funny', 'repita', 'Diga']
    answers_print = ['print', 'screenshot', 'tire uma foto da tela']
    answers_sair = ['sair', 'fechar', 'saiu', 'fechou', 'desligar']
    answers_restart = ['reiniciar', 'reinicie', 'restart', 'reset']
    answers_ReadTempNote = ['leia a nota temporária', 'diga a nota temporária', 'Diga a nota temporária']
    answers_tempnote = ['nota temporaria', 'crie uma nota temporaria', 'faça uma nota temporaria', 'mota temporaria', 'nota temporária']
    answers_speednet = ['speedtest', 'velocidade da internet', 'teste de velocidade', 'velocidade da net', 'speed test']
    answers_window = ['pegar janela', 'janela', 'window']
    answers_poweroff = ['desligar computador', 'reiniciar computador', 'deslogar']
    answers_joquempo = ['joquempo', 'pedra papel tesoura', 'joquempô']
    answers_wikipedia = ['wikipedia']
    answers_play = ['tocar audio', 'play']
    answers_local_playlist = ['tocar', 'tocar playlist', 'playlist local', 'tocar playlist local', 'playlist']
    answers_stop_song = ['parar musíca', 'parar musica', 'parar som']
    answers_limpar = ['limpar', 'cls', 'clear']
    answers_timer = ['timer', 'temporizador']
    answers_cronômetro = ['cronômetro', 'cronometre']
    answers_changelog = ['changelog']
    answers_maidutils = ['maidutils']
    answers_maidrecheck = ['recheck']
    answers_volume = ['']
else:
    import json
    config.read(f'{path}/Userdata/Configurações/Prefixos.ini')
    answers_cancelar = json.loads(config.get("Prefixos", "prefixo-cancelar"))
    answers_hora = json.loads(config.get("Prefixos", "prefixo-tempo"))
    answers_data = json.loads(config.get("Prefixos", "prefixo-data"))
    answers_dado = json.loads(config.get("Prefixos", "prefixo-dado"))
    answers_say = json.loads(config.get("Prefixos", "prefixo-fala"))
    answers_print = json.loads(config.get("Prefixos", "prefixo-print"))
    answers_sair = json.loads(config.get("Prefixos", "prefixo-sair"))
    answers_restart = json.loads(config.get("Prefixos", "prefixo-reiniciar"))
    answers_tempnote = json.loads(config.get("Prefixos", "prefixo-nota-temporaria"))
    answers_ReadTempNote = json.loads(config.get("Prefixos", "prefixo-ler-nota-temporaria"))
    answers_speednet = json.loads(config.get("Prefixos", "prefixo-speedtest"))
    answers_window = json.loads(config.get("Prefixos", "prefixo-controle-janela"))
    answers_poweroff = json.loads(config.get("Prefixos", "prefixo-desligar-pc"))
    answers_joquempo = json.loads(config.get("Prefixos", "prefixo-joquempo"))
    answers_volume = json.loads(config.get("Prefixos", "prefixo-volume"))
    answers_wikipedia = json.loads(config.get("Prefixos", 'prefixo-wikipedia'))
    answers_local_playlist = json.loads(config.get("Prefixos", 'prefixo-playlist-local'))
    answers_play = json.loads(config.get('Prefixos', 'prefixo-tocar-som'))
    answers_stop_song = json.loads(config.get("Prefixo", 'prefixo-parar-musica'))
    answers_limpar = json.loads(config.get("Prefixos", "prefixo-limpar-terminal"))
    answers_timer = json.loads(config.get("Prefixos", "prefixo-temporizador"))
    answers_cronômetro = json.loads(config.get("Prefixos", "prefixo-cronômetro"))
    answers_changelog = json.loads(config.get("Prefixos", 'prefixo-changelog'))
    answers_maidutils = json.loads(config.get("Prefixos", 'prefixo-inicializar-maidutils'))

#################################################
#A seguir se encontram coisas da maidutils. Isso só será executado se os módulos dela estiverem ativados    

maidutils_modules_activated = config.get('MaidUtils', 'modules').lower()

if maidutils_modules_activated == 'false':
    pass
else:
    if config.get('Geral', 'custom-prefixes').lower() == 'true':
        config.read(f'{path}/Userdata/Configurações/Prefixos.ini')
    else:
        if os.path.isfile(f'{path}/Userdata/Maid/Session/prefixes1.bin') == False: #Caso o user use prefixos padrão
            with open(f'{path}/Userdata/Maid/Session/prefixes1.bin', 'w') as f:  #Cria um prefixes1.bin caso não exista e joga os prefixos do módulo lá
                f.write()
        config.read(f'{path}/Userdata/Maid/Session/prefixes1.bin')
    
    if config.has_section('Modules') == False:
        config.add_section('Modules')
    
    maidutils_module_prefixes = []
    maidutils_module_names = []
    for key in config['Modules']:
        module_prefix = config.get('Modules', key)
        module_name = key.join(['=', f'{module_prefix}'])
        
        maidutils_module_prefixes.append(module_prefix)
        maidutils_module_names.append(module_name)