def grab(): #Pega imagens de um site
    import os, sys, configparser, datetime
    import urllib.parse as urlparse
    import requests
    from bs4 import BeautifulSoup

    config = configparser.ConfigParser(allow_no_value=True)

    ################################################################

    if os.path.isfile('./Configurações.ini') == False:
        config['Geral'] = {
        '; Ignora links cujo nao contem "https://" ou "http://".': None,
        'ignorar-links-nao-html': 'False',
        '; Caso esteja como "True", define "https://" acima de "http://"': None,
        'preferir-https': 'False',
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    ################################################################

    config.read('./Configurações.ini')
    config1 = config.get('Geral', 'ignorar-links-nao-html').lower() #Ignora links sem https no começo
    config2 = config.get('Geral', 'preferir-https').lower() #Quando o link n tem html, coloca http ao invés de https

    ################################################################

    if os.path.isfile('./links.txt') == False: #Cria links.txt
        with open('links.txt', 'w') as txt:
            txt.write('')

    if os.path.isdir('./Downloads') == False: #Cria Downloads
        os.mkdir('./Downloads')

    ################################################################    

    links = []
    with open ('links.txt', 'r') as txt: #Lê as linhas
        leitura = txt.read() #Lê arquivo de texto
        leitura2 = leitura.split("\n") #Separa linhas por \n (quebra de linha)
        for i in leitura2: #to com preguiça de faze melhor, depois arrumo
            links.append(i) #Coloca cada linha em uma array

    if not links: #Caso o links.txt esteja vazio
        print("Nenhum link foi encontrado!")
        print("Insira os links que deseja escanear no arquivo \"Links.txt\".")
    
    ################################################################

    imagens = []
    numero_imagem = 1
    numero_download = 1 #Numero que será colocado no nome da pasta do site. Aumenta a cada loop

    for i in links:
        try:
            nome_da_pasta = 'Site-{}-[{}]'.format(numero_download, datetime.datetime.now())
            os.mkdir(f'./Downloads/{nome_da_pasta}') #Cria pasta onde as imagens vão ficar
            numero_download = numero_download + 1

            print(f"Escaneando {i}...")
            
            request_get = requests.get(i)                            #Manda o get pro site
            soup = BeautifulSoup(request_get.content, 'html.parser') #Lê o html
            links2 = soup.find_all('img', src=True)                  #Pega todas as tags <img>, incluindo a source

    ################################################################

            for i in links2: #Lê todas as tags <img> encontradas pelo bs4

                print(f"Imagem obtida! Imagem = {numero_imagem}")

                if i['src'].find('https://') != -1 or i['src'].find('http://') != -1: #Checa se a src da tag tem http
                    request = requests.get(i['src']) #Pega a src da tag

                else:
                    if config1 == 'true': #Se o usuario escolheu n pegar link sem http, pula o item
                        continue
                    else: 

                        hostname = urlparse.urlparse(f'{i}').hostname #Pega o hostname do link

                        if config2 == 'true':
                            link_novo = ''.join(['https://', f'{hostname}', f'{i["src"]}']) #Junta htpps, hostname, e link
                        else:
                            link_novo = ''.join(['http://', f'{hostname}', f'{i["src"]}']) #Junta htpp, hostname, e link

                        request = request.get(link_novo) #Pega o link criado

    ################################################################

                with open('./Downloads/{}/img-{}'.format(nome_da_pasta, numero_imagem), 'wb') as output: #Salvando imagem
                    output.write(request.content)
                    output.close()
                    numero_imagem = numero_imagem + 1
                    print("Imagem baixada com sucesso!")
                    del request
        except Exception as x:
            import traceback
            print(f"Um erro ocorreu enquanto a imagem {numero_imagem} era baixada. Pulando...")
            print(f"Erro: {x}")
            print(traceback.format_exc())
    print("Operação concluida!")