def Joquempo():
    from MaidUtils.init.tts import say          #Importando função do tts
    from MaidUtils.init.voice import capture    #Importando função de captura de fala
    import random
    
    opções = ['pedra', 'papel', 'tesoura', 'cancelar', 'sair'] #Opções disponiveis para o jogador
    escolhas = ['pedra', 'papel', 'tesoura']                   #Opções disponiveis para a maid
    
    say("Que movimento deseja jogar?")
    
    while True:
        movimento = capture() #Pedindo para o jogador inserir o movimento desejado
        
        if movimento in escolhas:                               #Se o movimento tiver em escolhas
            if movimento == 'sair' or movimento == 'cancelar':  #Se o movimento for cancelar ou sair
                say("Cancelando...")                              
                break                                           #Cancela o joquempo
            else:
                maid_play = random.choice(escolhas)             #Maid escolhe uma jogada aleatória das opções dela
                
                if maid_play == 'pedra':                        #Se a maid escolher pedra
                    if movimento == 'papel':                    #Se a escolha do user for papel
                        say("Pedra, você ganhou!")              #Anuncia a vitória dele
                        break       
                    elif movimento == 'pedra':                  #Se a escolha do user for pedra
                        say('Pedra, deu empate!')               #Anuncia empate
                        break
                    else:                                       #Se a escolha do user for tesoura
                        say('Pedra, você perdeu!')              #Anuncia a perda dele
                        break
                    
                elif maid_play == 'tesoura':
                    if movimento == 'papel':
                        say("Tesoura, você perdeu!")
                        break
                    elif movimento == 'pedra':
                        say('Tesoura, você ganhou!')
                        break
                    else:
                        say('Tesoura, deu empate!')
                        break
                        
                elif maid_play == 'papel':
                    if movimento == 'papel':
                        say("Papel, deu empate!")
                        break
                    elif movimento == 'pedra':
                        say('Papel, você perdeu!')
                        break
                    elif movimento == 'tesoura':
                        say('Papel, você perdeu!')
                        break
        else:
            say("Jogada invalida. Que movimento deseja jogar?")