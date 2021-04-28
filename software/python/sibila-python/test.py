import logging
from managers.textmanager import TextManager
from rich.logging import RichHandler
from managers.knowledgemanager import KnowledgeManager
from managers.textmanager import TextManager
from entities.graphclasses import *
from rich import print,inspect
from rich.console import Console


def main():
    console = Console()
    console.clear()

    FORMAT = "%(message)s"
    #logging.basicConfig(level=logging.INFO,handlers=[RichHandler()])
    logging.basicConfig(
        level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    log = logging.getLogger("rich")
    #km = KnowledgeManager()
    tm = TextManager()
    km = KnowledgeManager()
    
    try:
        '''
        correcciones, error = tm.checkOrtografia("Prueva de tecto. Veamos que pasa con palavras divididas por un punto.O sin punto")
        #inspect(correcciones,title="TITULO",sort=False,methods=False)
        if error:
            print (correcciones)
            con_error = [c for c in correcciones if c['error']]
            print (con_error)
        else:
            print ("Todo correcto")
        '''
        
        
        tm.addWordsToDict(['POO','PPR','OOP','member'])
        texto = "Los objetos son parte del paradigma POO y están formados por métodos y atributos y se comunican por medio de mensajes"
        #print (tm.check(texto=texto))
        '''
        print (tm.tokenize(texto))
        '''
        #words = ['POO','EsUn','PARADIGMA','TEST','MARTIN','PRUEBA','TieneUn','Referencia','Utiliza']
        #print(km.setClass(word=words[0]))
        #print(km.setClasses (words=words))
        correcciones,tokens = km.tokenizeRespuesta(texto=texto,textManager=tm,includeStopWords=True)
        print (correcciones,tokens)
        tkn_str = [ (tk['text'],tk['lema'],tk['claseDB'],tk['claseSugerida']) for tk in tokens ]
        print (tkn_str)

    except Exception as e:
        inspect (e)
        log.exception(e)

if __name__ == '__main__':
    main()