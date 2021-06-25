import logging
from rich import print,inspect
from rich.logging import RichHandler
from managers.knowledgemanager import KnowledgeManager
from managers.textmanager import TextManager
import os

FORMAT = "%(message)s"
#logging.basicConfig(level=logging.INFO,handlers=[RichHandler()])
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

km = KnowledgeManager(
    host=os.getenv('PB_DB_HOST','http://localhost'),       # HOST
    port=os.getenv('PB_DB_PORT',2480),              # PORT
    user=os.getenv('PB_DB_USER','admin'),           # USER
    password=os.getenv('PB_DB_PASS','admin')        # PASSWORD
)

#gm = GraphicManager()

tm = TextManager()

correcciones,tokens = km.tokenizeRespuesta(
    texto="Una sentencia es verdadera si todo su contenido interno es coherente y real",
    textManager=tm,
    includeStopWords=False)
res = {
    "correcciones" : correcciones,
    "terminos" : tokens
}

inspect(res)