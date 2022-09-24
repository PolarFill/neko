def Time(): #Retorna o horario atual
    from datetime import datetime
    from MaidUtils.init.tts import say
    
    horas = datetime.now().strftime("%H")       #Pega as horas
    minutos = datetime.now().strftime("%M")     #Pega os minutos
    segundos = datetime.now().strftime("%S")    #Pega os segundos
    
    say("Agora são {} horas, {} minutos, e {} segundos.".format(horas, minutos, segundos))
    
def Date(): #Retorna o dia
    from datetime import datetime
    from MaidUtils.init.tts import say
    
    dia = datetime.now().strftime("%d")     #Pega o dia
    mês = datetime.now().strftime("%m")     #Pega o mês
    ano = datetime.now().strftime("%Y")     #Pega o ano
    formatado = datetime.now().strftime("%d/%m/%Y")
    weekday = WeekDay(dia, mês, ano)
    
    print('A data atual é {}, {}'.format(weekday, formatado))
    say("Hoje é {}, dia {} do {} de {}".format(weekday, dia, mês, ano), out=False)
    
def WeekDay(ano, mes, dia): #Retorna o dia da semana
    from datetime import date

    dia = date.isoweekday(date.today())
    
    if dia == 1:
        return 'segunda'
    elif dia == 2:
        return 'terça'
    elif dia == 3:
        return 'quarta'
    elif dia == 4:
        return 'quinta'
    elif dia == 5:
        return 'sexta'
    elif dia == 6:
        return 'sabado'
    elif dia == 7:
        return 'domingo'
    
def Timer(tempo): #Nome da função é alto-explicativo, mas é um cronometro
    import time, re
    from MaidUtils.init.tts import say      #Importando função do tts
    
    if 'horas' in tempo or 'hora' in tempo:
        tempo = re.sub('\D', '', tempo)     #Retira letras do tempo
        tempo = int(tempo)                  #Converte o tempo para int
        tempo = tempo * 60 * 60             #Converte horas pra segundo
        
    elif 'minutos' in tempo or 'minuto' in tempo:
        tempo = re.sub('\D', '', tempo)     #Retira letras do tempo
        tempo = int(tempo)                  #Converte o tempo para int
        tempo = tempo * 60

    elif 'segundos' in tempo or 'segundo' in tempo:
        tempo = re.sub('\D', '', tempo)     #Retira letras do tempo
        tempo = int(tempo)                  #Converte o tempo para int
        pass
    
    say("Iniciando temporizador...")
    time.sleep(tempo)
    say("Tempo do temporizador esgotado!")
    
def Cronometro():
    print("")