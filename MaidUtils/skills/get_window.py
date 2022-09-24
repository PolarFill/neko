def Manipulate(): #Função responsavel pela manipulação de janelas
    import platform
    from MaidUtils.init.tts import say  #Importando função do tts
    
    if platform.system() != 'Windows': #Infelizmente, esse módulo só funciona no windows. Checa se o OS é windows.
        say('Desculpe, esta função não é suportada no seu sistema')
    else:    
        
        from MaidUtils.init.voice import capture  #Importando função de captura de fala
        import pygetwindow as gw
        
        say('Que ação deseja realizar?')
        cmd = capture()
        
        cancel = ["cancelar", 'parar', 'cancele', 'pare']
        restore = ['restaurar', 'restaurar', 'restaurar janela']
        close = ['fechar', 'feche', 'saia', 'sair']
        maximize_list = ['maximizar', 'maximize', 'aumentar', 'aumente']
        minimize_list = ['minimizar', 'minimize', 'esconda', 'tire']
        minimize_all = ['minimize tudo', 'minimize todas', 'minimizar janelas', 'minimizar tudo']
        maximize_all = ['maximize tudo', 'maximize todas', 'maximize janelas']
        close_all = ['fechar tudo', 'fechar todas', 'sair tudo', 'sair todas', 'feche tudo', 'feche todas']
        
        if cmd in maximize_list:                            #Maximizar janela
            active = gw.getActiveWindow()
            say("Maximizando janela...")
            active.maximize()
                
        elif cmd in minimize_list:  #Minimiza todas as janelas
            active = gw.getActiveWindow()
            say("Minimizando janela...")
            active.minimize()

        elif cmd in minimize_all:           #Minimiza todas as janelas
            active = gw.getAllWindows()     #Pega todas as janelas
            say("Minimizando janelas...")   
            active.minimize()               #Minimiza elas

        elif cmd in maximize_all:       #Maximiza todas as janelas
            active = gw.getAllWindows() #Pega todas as janelas
            say("Maximizando janelas...")
            active.maximize()           #Maximiza elas
            
        elif cmd in close:  #Fecha a janela
            active = gw.getActiveWindow()
            say("Fechando janela...")
            active.close()
            
        elif cmd in close_all:
            active = gw.getAllWindows()
            say("Fechando janelas...")
            active.close()
        
        elif cmd in restore:
            active = gw.getActiveWindow()
            say("Restaurando janela...")
            active.restore()
            
        elif cmd in cancel:
            pass
        
        else:
            say("Desculpe, não entendi.")
            pass