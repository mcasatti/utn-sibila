import hunspell     # Usa cyhunspell en lugar del original hunspell. Ver requirements.txt
import os
import re
from rich import print, inspect
import spacy

class TextManager:

    TEXT_MANAGER_BASE_DIR = None
    HUNSPELL_DICTIONARIES = None
    dic = None
    nlp = None

    def __init__ (self):
        # Inicializa el directorio donde están los diccionarios
        self.TEXT_MANAGER_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.HUNSPELL_DICTIONARIES = self.TEXT_MANAGER_BASE_DIR+"/res/hunspell-es/"
        self.nlp = spacy.load('es_core_news_sm')
        self.dic = hunspell.Hunspell(self.HUNSPELL_DICTIONARIES + "es_ANY")

        #print (self.TEXT_MANAGER_BASE_DIR)
        #print (self.HUNSPELL_DICTIONARIES)


    def checkOrtografia (self, texto : str, full : bool = False):
        error = False
        correcciones = []
        #palabras = texto.split()
        palabras = re.findall(r"[a-z\-]+",texto)
        tokens = self.nlp(texto)
        #inspect(tokens)
        palabras = [token.text for token in tokens]
        #print (palabras)
        #print([(token.text, token.pos_, token.tag_, token.lemma_, token.norm_, token.is_punct) for token in tokens])
        #print (tokens)
        
        for sequence,palabra in enumerate(palabras):
            correcta = self.dic.spell(palabra)
            sugerencias = self.dic.suggest(palabra) if not correcta else []
            correcciones.append({
                "sequence": sequence,
                "original": palabra,
                "error": not correcta,
                "sugerencias": sugerencias
            })

            if not correcta:
                error = True
        # Si no pido el resultado full, devuelvo solo los errores
        if not full:
            correcciones = [c for c in correcciones if c['error']]
            
        return correcciones, error

