def Wikipedia(search, keyword=None):
    from mediawiki import MediaWiki #Importando wrapper da mediawiki api
    wikipedia = MediaWiki()
    
    try:
        if keyword != None: #Se o usuario não falou nada que ele queira pesquisar
            wikipedia.opensearch(search, results=1)
        else:
            wikipedia.page(search)
    except:
        pass