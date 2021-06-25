import hunspell     # Usa cyhunspell en lugar del original hunspell. Ver requirements.txt
import os
import re
from rich import print, inspect
import spacy
from typing import List, Text, Tuple

class TextException (Exception):
    message : str = None
    def __init__(self,message : str):
        self.message = message
        super().__init__(self.message)

'''
TODO: Estudiar la posibilidad de no utilizar CyHunspell para la corrección ortográfica sino 
symspellpy: https://symspellpy.readthedocs.io/en/latest/index.html
https://github.com/wolfgarbe/SymSpell
Esta librería es más rápida y flexible que hunspell 
'''
class TextManager:

    TEXT_MANAGER_BASE_DIR = None
    HUNSPELL_DICTIONARIES = None
    dic = None
    nlp = None
    mapPOS = None
    ownDictionary = []

    def __init__ (self):
        # Inicializa el directorio donde están los diccionarios
        self.TEXT_MANAGER_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.HUNSPELL_DICTIONARIES = self.TEXT_MANAGER_BASE_DIR+"/res/hunspell-es/"
        self.nlp = spacy.load('es_core_news_sm')
        self.dic = hunspell.Hunspell(self.HUNSPELL_DICTIONARIES + "es_ANY")
        self.ownDictionary = set()
        
        self.mapPOS = {
            "ADJ" : "ADJETIVO",
            "ADP" : "ADPOSICION",
            "ADV" : "ADVERBIO",
            "AUX" : "AUXILIAR",
            "CONJ": "CONJUNCION",
            "DET" : "DETERMINANTE",
            "INTJ": "INTERJECCION",
            "NOUN": "SUSTANTIVO",
            "NUM" : "NUMERAL",
            "PART": "PARTICULA",
            "PRON": "PRONOMBRE",
            "PROPN":"PRONOMBRE PROPIO",
            "PUNCT":"PUNTUACION",
            "SCONJ":"CONJUNCIÓN SUBORDINADA",
            "SYM" : "SIMBOLO",
            "VERB": "VERBO",
            "CCONJ" : "CONJUNCION COORDINANTE",
            "X" : "OTRO"
        }
        
    def isOkOrtografia (self, texto : str) -> bool:
        tokens = self.nlp(texto)
        palabras = [token.text for token in tokens]
        for palabra in palabras:
            if not self.dic.spell(palabra):
                return False
        return True

    def __tokenize__ (self, texto : str):
        tokens = self.nlp(texto)
        return tokens

    def check (self, texto : str = None, full : bool = False, tokens: List=None):
        if not texto and not tokens:
            raise TextException ("Se debe proveer un texto o una lista de tokens a analizar")
        
        if not tokens:
            tokens = self.__tokenize__(texto)
        
        correcciones = []

        palabras = [token.text for token in tokens]
        
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

        # Si no pido el resultado full, devuelvo solo los errores
        if not full:
            correcciones = [c for c in correcciones if c['error']]
            
        return correcciones

    def addWordToDict (self, word : str):
        self.dic.add(word)
        self.ownDictionary.add(word)
        return {"result":"ok"}

    def addWordsToDict (self, words : List[str]):
        for word in words:
            self.addWordToDict(word)
            self.ownDictionary.add(word)
        return {"result":"ok"}

    def delWordFromDict (self, word : str):
        self.dic.remove(word)
        self.ownDictionary.remove(word)
        return {"result" : "ok"}

    def getDictionary (self):
        return self.ownDictionary

    '''
    METODOS de gestión de tokens (Spacy)
    '''
    def translatePOS (self, pos : str)-> Tuple[str,str]:
        return self.mapPOS[pos]

    def tokenize (self, texto : str) -> str:
        tkns = self.nlp(texto)
        correcciones = self.check(tokens=tkns)

        tokens = []
        for tkn in tkns:
            token = {
                    "text" : tkn.text,
                    "head" : tkn.head.text,
                    "ent_type" : tkn.ent_type_,
                    "pos": tkn.pos_,
                    "trans_pos": self.translatePOS(tkn.pos_),
                    "lema" : tkn.lemma_,
                    "norm": tkn.norm_,
                    "depends": tkn.dep_,
                    "prob": tkn.prob,
                    "sentiment": tkn.sentiment,
                    "stop": tkn.is_stop
                }
            tokens.append(token)
        
        return correcciones, tokens
        