/*
 * ESTRUCTURAS DEFINIDAS EN EL GRAFO 2 PARA CALCULO DE MÉTRICAS Y ANÁLISIS DE PATRONES
 */

/************************************************
 * EVALUACION
 ************************************************/
create class CEvaluacion if not exists extends V;
create property CEvaluacion.numero string (notnull true);
create property CEvaluacion.nombre string (notnull true);
create property CEvaluacion.fecha Date (notnull true);
create property CEvaluacion.tipo string (notnull true);		/* PARCIAL, FINAL, CONTENIDO */
create property CEvaluacion.cicloLectivo integer (notnull true);

/************************************************
 * RELACION SIMPLE
 ************************************************/
create class RSimple if not exists extends E;
create property RSimple.nombre string (notnull true);

/************************************************
 * PREGUNTA
 ************************************************/
create class CPregunta if not exists extends V;
create property CPregunta.numero string (notnull true);
create property CPregunta.texto string (notnull true);
create property CPregunta.unidadTematicaNumero integer;
create property CPregunta.unidadTematicaNombre string;
create property CPregunta.puntuacion integer;

/************************************************
 * RESPUESTA
 ************************************************/
create class CRespuesta if not exists extends V;
create property CRespuesta.numero integer;
create property CRespuesta.texto string (notnull true);
create property CRespuesta.tipo string (notnull true);		/* BASE, DE ALUMNO, DE CONTENIDO */
create property CRespuesta.comision string;
create property CRespuesta.puntaje float;

/************************************************
 * RELACION FUZZY
 ************************************************/
create class RFuzzy if not exists extends E;
create property RFuzzy.nombre string;

/************************************************
 * CONCEPTO FUZZY
 ************************************************/
create class CFuzzy if not exists extends V;
create property CFuzzy.nombre string;

/************************************************
 * TERMINO
 ************************************************/
create class CTermino if not exists extends V;
create property CTermino.nombre string;
create property CTermino.lema string (notnull true);
create property CTermino.inRespuestas EMBEDDEDLIST;		/* Lista de los identificadores de las preguntas en donde aparece, id de orientdb de tipo #xx:xxx */


create class RTermino if not exists extends E;
create property RTermino.nombre string (notnull true);
create property RTermino.lema string (notnull true);
create property RTermino.inRespuestas EMBEDDEDLIST;



