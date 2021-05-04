from typing import Dict, List,Tuple
from .dbmanager import DBManager
from .textmanager import TextManager
from entities.graph2classes import *
import re
import json
from rich import print,inspect

class KmException (Exception):
    message : str = None
    def __init__(self,message : str):
        self.message = message
        super().__init__(self.message)

class Knowledge2Manager:
    db : DBManager = None
    db2: DBManager = None
    mapTipoTermino : None
        
    
    """
    Concept Manager:
    Clase que engloba todas las operaciones de gestión de conceptos y relaciones en OrientDB
    """
    def __init__ (self, host='http://localhost', port=2480, database='sibila-patterns', user='admin', password='admin', database2=None, user2=None, password2=None):        
        self.db = DBManager(host=host,port=port,database=database,user=user,password=password)
        if database2:
            self.db2 = DBManager(host=host,port=port,database=database2,user=user2,password=password2)
        '''
        Mapping de los tipos de termino.
        Documentacion detallada: 
        https://universaldependencies.org/es/index.html
        https://universaldependencies.org/docs/u/pos/
        '''
        self.mapTipoTermino = {
            "ADJETIVO":"CONCEPTO",
            "ADPOSICION": "",
            "ADVERBIO":"RELACION",
            "AUXILIAR":"RELACION",
            "CONJUNCION":"RELACION",
            "DETERMINANTE":"",
            "INTERJECCION":"",
            "SUSTANTIVO":"CONCEPTO",
            "NUMERAL":"CONCEPTO",
            "PARTICULA":"",
            "PRONOMBRE":"",
            "PRONOMBRE PROPIO":"CONCEPTO",
            "PUNTUACION":"",
            "CONJUNCIÓN SUBORDINADA":"RELACION",
            "SIMBOLO":"CONCEPTO",
            "VERBO":"RELACION",
            "CONJUNCION COORDINANTE":"RELACION",
            "OTRO":""
        }
    
    '''
    Los VERBOS de la gestión de la base de conocimiento van a ser:
    INS: Insertar un nuevo registro
    DEL: Eliminar un registro existente
    UPD: Modificar un registro existente
    GET: Obtener información
    '''
    '''
    -----------------------------------------------------------------------------------------
    TODO: TODOS LOS METODOS QUE INSERTEN O ACTUALICEN INFORMACION DE ENTIDADES DEBEN DEVOLVER
    EN EL RETORNO, UN OBJETO CON LOS DATOS ACTUALIZADOS
    ''' 
#--------------------------------------------------------------------------------------------------------------------------
    # GESTION DE Vertices
# -------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
    # GESTION DE CEvaluacion
# --------------------------------------------------------------------------------------------
    def insCEvaluacion (self,cEvaluacion : CEvaluacion) -> Tuple[str,int]:
        result,id = self.db.insVertex(
            classname="CEvaluacion",
            fields={
                "cicloLectivo": cEvaluacion.cicloLectivo,
                "fecha": cEvaluacion.fecha,
                "nombre": cEvaluacion.nombre,
                "numero": cEvaluacion.numero,
                "tipo": cEvaluacion.tipo
                }
            )
        return result,id

    def updCEvaluacion (self,oldCEvaluacion : CEvaluacion,newCEvaluacion : CEvaluacion) -> Tuple[str, int]:
        result = self.db.updVertex(
            classname="CEvaluacion",
            keys={
                "nombre": oldCEvaluacion.nombre
            },
            fields={
                "cicloLectivo": newCEvaluacion.cicloLectivo,
                "fecha": newCEvaluacioo.fecha,
                "nombre": newCEvaluacion.nombre,
                "numero": newCEvaluacion.numero,
                "tipo": newCEvaluacion.tipo
                }
            )
        if result:
            # El update no devuelve un ID sino la cantidad de registros afectados
            count = self.db.extractCount(result)
        else:
            count = 0
        return result,count

    def delCEvaluacion (self,cEvaluacion : CEvaluacion, safe : bool=True) -> Tuple[str,int]:
        result = None
        count = 0
        if safe:
            if not self.isSafeDelete(cEvaluacion):
                raise Exception("El CEvaluacion tiene relaciones, no es posible eliminarlo")

        result = self.db.delVertex(
            classname="CEvaluacion",
            keys={
                "nombre": cEvaluacion.nombre,
            })
        if result:
            # El delete no devuelve un ID sino la cantidad de registros afectados
            count = self.db.extractCount(result)
        else:
            count = 0
        return result,count

    def isSafeDelete (self, cEvaluacion : CEvaluacion) -> bool:
        r = self.getRefsCEvaluacion(cEvaluacion)
        return r == 0
        # Probando, porque por algun motivo la linea de abajo cree que es una tupla
        # return bool(refs == 0)

    def getRefsCEvaluacion (self,cEvaluacion : CEvaluacion) -> int:
        '''
        La funcion obtiene la cantidad de referencias (entrantes y salientes) de un cEvaluacion dado.
        Si no encuentra el cEvaluacion devuelve 0
        '''
        query = "match {{class: CEvaluacion, as: c, where: (nombre = '{nombre}')}} return (c.in().size()+c.out().size()) as referencias".format(nombre=cEvaluacion.nombre)
        result = self.db.execCommand(query)
        if result:
            referencias = result[0]["referencias"]
            return referencias
        else:
            return 0

    def getCEvaluacion (self, keys : Dict = None, limit : int = 0):
        if keys:
            condicion = self.db.__getWhereFromDict__(keys)
        else:
            condicion = '1=1'
        if limit:
            limite = 'LIMIT {limit}'.format(limit=limit)
        else:
            limite = ''
        query = "match {{class: CEvaluacion, as: c, where: ({condicion})}} return expand(c) as result {limite}".format(condicion=condicion,limite=limite)
        result = self.db.execCommand(query)
        if result:
            return result
        else:
            return None

    def getCEvaluacionByName (self,name : str):
        return self.getCEvaluacion(keys={"nombre":name})

#--------------------------------------------------------------------------------------------
    # GESTION DE CFuzzy
# --------------------------------------------------------------------------------------------
    def insCFuzzy (self,cFuzzy : CFuzzy) -> Tuple[str,int]:
        result,id = self.db.insVertex(
            classname="CFuzzy",
            fields={                
                "nombre": cFuzzy.nombre                
                }
            )
        return result,id

    def updCFuzzy (self, oldCFuzzy : CFuzzy, newCFuzzy : CFuzzy) -> Tuple[str, int]:
        result = self.db.updVertex(
            classname="CFuzzy",
            keys={
                "nombre": oldCFuzzy.nombre
            },
            fields={
                "nombre": newCFuzzy.nombre                
                }
            )
        if result:
            # El update no devuelve un ID sino la cantidad de registros afectados
            count = self.db.extractCount(result)
        else:
            count = 0
        return result,count

    def delCFuzzy (self,cFuzzy : CFuzzy, safe : bool=True) -> Tuple[str,int]:
        result = None
        count = 0
        if safe:
            if not self.isSafeDelete(cFuzzy):
                raise Exception("El CFuzzy tiene relaciones, no es posible eliminarlo")

        result = self.db.delVertex(
            classname="CFuzzy",
            keys={
                "nombre": cFuzzy.nombre,
            })
        if result:
            # El delete no devuelve un ID sino la cantidad de registros afectados
            count = self.db.extractCount(result)
        else:
            count = 0
        return result,count

    def isSafeDelete (self, cFuzzy : CFuzzy) -> bool:
        r = self.getRefsCFuzzy(cFuzzy)
        return r == 0
        # Probando, porque por algun motivo la linea de abajo cree que es una tupla
        # return bool(refs == 0)

    def getRefsCFuzzy (self,cFuzzy : CFuzzy) -> int:
        '''
        La funcion obtiene la cantidad de referencias (entrantes y salientes) de un cFuzzy dado.
        Si no encuentra el cFuzzy devuelve 0
        '''
        query = "match {{class: CFuzzy, as: c, where: (nombre = '{nombre}')}} return (c.in().size()+c.out().size()) as referencias".format(nombre=cFuzzy.nombre)
        result = self.db.execCommand(query)
        if result:
            referencias = result[0]["referencias"]
            return referencias
        else:
            return 0

    def getCFuzzy (self, keys : Dict = None, limit : int = 0):
        if keys:
            condicion = self.db.__getWhereFromDict__(keys)
        else:
            condicion = '1=1'
        if limit:
            limite = 'LIMIT {limit}'.format(limit=limit)
        else:
            limite = ''
        query = "match {{class: CFuzzy, as: c, where: ({condicion})}} return expand(c) as result {limite}".format(condicion=condicion,limite=limite)
        result = self.db.execCommand(query)
        if result:
            return result
        else:
            return None

 #--------------------------------------------------------------------------------------------
    # GESTION DE CPregunta
# --------------------------------------------------------------------------------------------
    def insCPregunta (self,cPregunta : CPregunta) -> Tuple[str,int]:
        result,id = self.db.insVertex(
            classname="CPregunta",
            fields={
                "numero": cPregunta.numero,
                "puntuacion": cPregunta.puntuacion,
                "texto": cPregunta.texto,
                "unidadTematicaNombre": cPregunta.unidadTematicaNombre,
                "unidadTematicaNumero": cPregunta.unidadTematicaNumero                
                }
            )
        return result,id

    def updCPregunta (self,oldCPregunta : CPregunta, newCPregunta : CPregunta) -> Tuple[str, int]:
        result = self.db.updVertex(
            classname="CPregunta",
            keys={
                "numero": oldCPregunta.numero
            },
            fields={
                "numero": newCPregunta.numero,
                "puntuacion": newCPregunta.puntuacion,
                "texto": newCPregunta.texto,
                "unidadTematicaNombre": newCPregunta.unidadTematicaNombre,
                "unidadTematicaNumero": newCPregunta.unidadTematicaNumero  
                }
            )
        if result:
            # El update no devuelve un ID sino la cantidad de registros afectados
            count = self.db.extractCount(result)
        else:
            count = 0
        return result,count

    def delCPregunta (self,cPregunta : CPregunta, safe : bool=True) -> Tuple[str,int]:
        result = None
        count = 0
        if safe:
            if not self.isSafeDelete(cPregunta):
                raise Exception("El CPregunta tiene relaciones, no es posible eliminarlo")

        result = self.db.delVertex(
            classname="CPregunta",
            keys={
                "numero": cPregunta.numero,
            })
        if result:
            # El delete no devuelve un ID sino la cantidad de registros afectados
            count = self.db.extractCount(result)
        else:
            count = 0
        return result,count

    def isSafeDelete (self, cPregunta : CPregunta) -> bool:
        r = self.getRefsCPregunta(cPregunta)
        return r == 0

    def getRefsCPregunta (self,cPregunta : CPregunta) -> int:
        '''
        La funcion obtiene la cantidad de referencias (entrantes y salientes) de un cPregunta dado.
        Si no encuentra el cPregunta devuelve 0
        '''
        query = "match {{class: CPregunta, as: c, where: (numero = '{numero}')}} return (c.in().size()+c.out().size()) as referencias".format(numero=cPregunta.numero)
        result = self.db.execCommand(query)
        if result:
            referencias = result[0]["referencias"]
            return referencias
        else:
            return 0

    def getCPregunta (self, keys : Dict = None, limit : int = 0):
        if keys:
            condicion = self.db.__getWhereFromDict__(keys)
        else:
            condicion = '1=1'
        if limit:
            limite = 'LIMIT {limit}'.format(limit=limit)
        else:
            limite = ''
        query = "match {{class: CPregunta, as: c, where: ({condicion})}} return expand(c) as result {limite}".format(condicion=condicion,limite=limite)
        result = self.db.execCommand(query)
        if result:
            return result
        else:
            return None

    def getCPreguntaByTexto (self, text : str):
        return self.getCPregunta(keys={"texto":text})

#--------------------------------------------------------------------------------------------
    # GESTION DE CRespuesta
# --------------------------------------------------------------------------------------------
    def insCRespuesta (self,cRespuesta : CRespuesta) -> Tuple[str,int]:
        result,id = self.db.insVertex(
            classname="CRespuesta",
            fields={
                "comision": cRespuesta.comision,
                "numero": cRespuesta.numero,
                "puntaje": cRespuesta.puntaje,
                "texto": cRespuesta.texto,
                "tipo": cRespuesta.tipo
                }
            )
        return result,id

    def updCRespuesta (self,oldCRespuesta : CRespuesta,newCRespuesta : CRespuesta) -> Tuple[str, int]:
        result = self.db.updVertex(
            classname="CRespuesta",
            keys={
                "comision": oldCRespuesta.comision,
                "numero": oldCRespuesta.numero
            },
            fields={
                "comision": newCRespuesta.comision,
                "numero": newCRespuesta.numero,
                "puntaje": newCRespuesta.puntaje,
                "texto": newCRespuesta.texto,
                "tipo": newCRespuesta.tipo
                }
            )
        if result:
            # El update no devuelve un ID sino la cantidad de registros afectados
            count = self.db.extractCount(result)
        else:
            count = 0
        return result,count

    def delCRespuesta (self,cRespuesta : CRespuesta, safe : bool=True) -> Tuple[str,int]:
        result = None
        count = 0
        if safe:
            if not self.isSafeDelete(cRespuesta):
                raise Exception("El CRespuesta tiene relaciones, no es posible eliminarlo")

        result = self.db.delVertex(
            classname="CRespuesta",
            keys={
                "comision": cRespuesta.comision,
                "numero": cRespuesta.numero
            })
        if result:
            # El delete no devuelve un ID sino la cantidad de registros afectados
            count = self.db.extractCount(result)
        else:
            count = 0
        return result,count

    def isSafeDelete (self, cRespuesta : CRespuesta) -> bool:
        r = self.getRefsCRespuesta(cRespuesta)
        return r == 0
        # Probando, porque por algun motivo la linea de abajo cree que es una tupla
        # return bool(refs == 0)

    def getRefsCRespuesta (self,cRespuesta : CRespuesta) -> int:
        '''
        La funcion obtiene la cantidad de referencias (entrantes y salientes) de un cRespuesta dado.
        Si no encuentra el cRespuesta devuelve 0
        '''
        #----------------- Revisar QUERY PARA LA CRespuesta
        #query = "match {{class: CRespuesta, as: c, where: (Nombre = '{nombre}')}} return (c.in().size()+c.out().size()) as referencias".format(nombre=cRespuesta.nombre)
        result = self.db.execCommand(query)
        if result:
            referencias = result[0]["referencias"]
            return referencias
        else:
            return 0

    def getCRespuesta (self, keys : Dict = None, limit : int = 0):
        if keys:
            condicion = self.db.__getWhereFromDict__(keys)
        else:
            condicion = '1=1'
        if limit:
            limite = 'LIMIT {limit}'.format(limit=limit)
        else:
            limite = ''
        query = "match {{class: CRespuesta, as: c, where: ({condicion})}} return expand(c) as result {limite}".format(condicion=condicion,limite=limite)
        result = self.db.execCommand(query)
        if result:
            return result
        else:
            return None

    #Revisar con Martin
    # def getCRespuestaByName (self,name : str):
    #     return self.getCRespuesta(keys={"nombre":name})

#--------------------------------------------------------------------------------------------
    # GESTION DE CTermino
# --------------------------------------------------------------------------------------------
    def insCTermino (self,cTermino : CTermino) -> Tuple[str,int]:
        result,id = self.db.insVertex(
            classname="CTermino",
            fields={
                "inPreguntas": cTermino.inPreguntas,
                "lema": cTermino.lema,
                "nombre": cTermino.nombre
                            }
            )
        return result,id

    def updCTermino (self,oldCTermino : CTermino,newCTermino : CTermino) -> Tuple[str, int]:
        result = self.db.updVertex(
            classname="CTermino",
            keys={
                "nombre": oldCTermino.nombre
            },
            fields={
                "inPreguntas": newCTermino.inPreguntas,
                "lema": newCTermino.lema,
                "nombre": newCTermino.nombre                
                }
            )
        if result:
            # El update no devuelve un ID sino la cantidad de registros afectados
            count = self.db.extractCount(result)
        else:
            count = 0
        return result,count

    def delCTermino (self,cTermino : CTermino, safe : bool=True) -> Tuple[str,int]:
        result = None
        count = 0
        if safe:
            if not self.isSafeDelete(cTermino):
                raise Exception("El CTermino tiene relaciones, no es posible eliminarlo")

        result = self.db.delVertex(
            classname="CTermino",
            keys={
                "comision": cTermino.comision,
                "numero": cTermino.numero
            })
        if result:
            # El delete no devuelve un ID sino la cantidad de registros afectados
            count = self.db.extractCount(result)
        else:
            count = 0
        return result,count

    def isSafeDelete (self, cTermino : CTermino) -> bool:
        r = self.getRefsCTermino(cTermino)
        return r == 0
        # Probando, porque por algun motivo la linea de abajo cree que es una tupla
        # return bool(refs == 0)

    def getRefsCTermino (self,cTermino : CTermino) -> int:
        '''
        La funcion obtiene la cantidad de referencias (entrantes y salientes) de un cTermino dado.
        Si no encuentra el cTermino devuelve 0
        '''

        query = "match {{class: CTermino, as: c, where: (nombre = '{nombre}')}} return (c.in().size()+c.out().size()) as referencias".format(nombre=cTermino.nombre)
        result = self.db.execCommand(query)
        if result:
            referencias = result[0]["referencias"]
            return referencias
        else:
            return 0

    def getCTermino (self, keys : Dict = None, limit : int = 0):
        if keys:
            condicion = self.db.__getWhereFromDict__(keys)
        else:
            condicion = '1=1'
        if limit:
            limite = 'LIMIT {limit}'.format(limit=limit)
        else:
            limite = ''
        query = "match {{class: CTermino, as: c, where: ({condicion})}} return expand(c) as result {limite}".format(condicion=condicion,limite=limite)
        result = self.db.execCommand(query)
        if result:
            return result
        else:
            return None

    def getCTerminoByName (self,name : str):
        return self.getCTermino(keys={"nombre":name})

#--------------------------------------------------------------------------------------------------------------------------
    # GESTION DE Relaciones
# -------------------------------------------------------------------------------------------------------------------------