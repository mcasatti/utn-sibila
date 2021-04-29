from pydantic import BaseModel
from typing import Optional

##-----------------------------------------------------------------------------------
##  Vertex Clasess
##-----------------------------------------------------------------------------------
class CEvaluacion:
    cicloLectivo: int
    fecha: date
    nombre: str
    numero: str
    tipo: str

class CFuzzy:
    nombre: str

class CPregunta:    
    numero: str
    puntuacion: int
    texto: str
    unidadTematicaNombre: str
    unidadTematicaNumero: str

class CRespuesta:
    comision: str
    numero: int
    puntaje: float
    texto: str
    tipo: str

class CTermino:
    inPreguntas: list # EmnbeddedList
    lema: str
    nombre: str

##-----------------------------------------------------------------------------------
##  Edge Clasess
##-----------------------------------------------------------------------------------
class RFuzzy:
    nombre: str

class RSimple:
    nombre: str

class RTermino:
    inRespuesta: list
    lema: str
    nombre: str

##-----------------------------------------------------------------------------------
##  Generic Clasess
##-----------------------------------------------------------------------------------
class OSecurityPolicy:
    active: bool
    afterUpdate: str
    beforeUpdate: str
    create: str
    delete: str
    execute: str
    name: str
    read: str

    

