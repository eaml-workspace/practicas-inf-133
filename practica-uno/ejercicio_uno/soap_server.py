from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

def suma(numero1,numero2):
    c=numero1+numero2
    return c

def resta(numero1,numero2):
    c=numero1-numero2
    return c

def multiplicacion(numero1,numero2):
    c=numero1*numero2
    return c

def division(numero1,numero2):
    c=numero1/numero2
    return c

dispatcher = SoapDispatcher(
    "soap-server",
    location="http://localhost:8000/",
    action= "http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "SumaDosNumeros",
    suma,
    returns= {"suma": int},
    args={"numero1": int, "numero2": int},
)
dispatcher.register_function(
    "RestaDosNumeros",
    resta,
    returns= {"resta": int},
    args={"numero1": int, "numero2": int},
)
dispatcher.register_function(
    "MultiplicacionDosNumeros",
    multiplicacion,
    returns= {"multiplicacion": int},
    args={"numero1": int, "numero2": int},
)
dispatcher.register_function(
    "DivisionDosNumeros",
    division,
    returns= {"division": float},
    args={"numero1": int, "numero2": int},
)

server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP Iniciando en http://localhost:8000/")
server.serve_forever()