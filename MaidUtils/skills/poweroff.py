def Main(input):
    import subprocess #Executa o comando
    import platform #Determina o sistema do usuario
    
    if 'desligar' in cmd:
        if platform.system().startswith('W'):
            subprocess