def Init():
    import platform
    import configparser
    from config import path
    config = configparser.ConfigParser()
    config.read(f'{path}/Userdata/Configurações/Principal.ini')

    if config.get('Geral', 'admin').lower() == 'true' and platform.system() == 'Windows':
        import ctypes, sys
        check_admin = ctypes.windll.shell32.IsUserAnAdmin() #Checando se o usuario atual é admin usando ctypes
        if check_admin == 0:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1) #Reinicia a maid se n tiver adm
            exit()

    if config.get('Geral', 'mostrar-terminal').lower() == 'false' and platform.system() == 'Windows':
        import win32.lib.win32con as win32con #Importando win32con do pywin32
        import win32.win32gui as win32gui #Importando win32gui do pywin32
        program = win32gui.GetForegroundWindow() #Anexando a variavel "program" com a janela atual do terminal
        win32gui.ShowWindow(program, win32con.SW_HIDE) #Escondendo o terminal
    
    if config.get('Geral', 'patch-quickedit').lower() == 'true' and platform.system() == 'Windows':
        import ctypes
        kernel32 = ctypes.windll.kernel32 #Pegando dll
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128) #Mudando as configurações do console atual