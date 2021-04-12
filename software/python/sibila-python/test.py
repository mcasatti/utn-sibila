import logging
from rich.logging import RichHandler
from managers.knowledgemanager import KnowledgeManager
from entities.graphclasses import *
from rich import print,inspect


def main():
    FORMAT = "%(message)s"
    #logging.basicConfig(level=logging.INFO,handlers=[RichHandler()])
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    log = logging.getLogger("rich")
    km = KnowledgeManager()
    
    try:
        inspect (km.getConceptosComplejos())

        '''
        c1 = Concepto(Nombre="ConceptoExtraño")
        result, id = km.insConcepto(c1)
        print (result,id)
        conceptos = ['MODELO','DISEÑO','PROGRAMA','OBJETO']

        result = km.getPath(conceptoInicial=c1,conceptosIncluidos=conceptos)
        print (result)

        result = km.getPathsFrom(conceptoInicial=c1,profundidad=1)
        print (result)
        
        result = cm.getPathsByType(relacion=Relacion('EsUn'))
        print (result)
        '''
        # inspect(query)
    except Exception as e:
        inspect (e)
        log.exception(e)

if __name__ == '__main__':
    main()