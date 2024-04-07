from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs
#diccionarip
pacientes=[
    {
    "ci": 123456,
    "nombre": "Ema",
    "apellido": "Roberts",
    "edad": 40,
    "genero":"Femenino",
    "diagnostico":"Diabetes",
    "doctor":"Pedro-Pérez",
    },
    {
    "ci": 654321,
    "nombre": "Lupe",
    "apellido": "Lupita",
    "edad": 15,
    "genero":"Femenino",
    "diagnostico":"Gripe",
    "doctor":"Pedro-Páramo",
    }
]

class PacienteService:
    @staticmethod
    def find_paciente_ci(ci):
        return next(
            (paciente for paciente in pacientes if paciente["ci"] == ci),
            None,
        )
    
    @staticmethod
    def find_paciente_diagnostico(diagnostico):
        """pac=[]
        for index, paciente in pacientes:
            if paciente["diagnostico"] == diagnostico:
                pac.append(paciente)"""
        return next((paciente for paciente in pacientes if paciente["diagnostico"]== diagnostico),
            None
        )
    
    @staticmethod
    def find_paciente_doctor(doctor):
        return next(
            (paciente for paciente in pacientes if paciente["doctor"] == doctor),
            None
        )
    
    @staticmethod
    def add_paciente(data):
        pacientes.append(data)
        return pacientes

    @staticmethod
    def update_paciente(ci,data):
        paciente = PacienteService.find_paciente_ci(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        else:
            return None 
    
    @staticmethod
    def delete_paciente(ci):
        paciente = PacienteService.find_paciente_ci(ci)
        if paciente:
            pacientes.remove(paciente)
            return pacientes
        else:
            return None


class HTTPResponseHandler:
    @staticmethod
    def handle_response(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

class PacienteRequestHandler(BaseHTTPRequestHandler):
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados= PacienteService.find_paciente_diagnostico(diagnostico)
                if pacientes_filtrados != []:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "doctor" in query_params:            
                doctor = query_params["doctor"][0]
                pacientes_filtrados= PacienteService.find_paciente_doctor(doctor)
                if pacientes_filtrados != []:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            
        elif self.path.startswith("/pacientes/"):
            ci= int(self.path.split("/")[-1])
            paciente = PacienteService.find_paciente_ci(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error":"Ruta no existente"})
    
    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes = PacienteService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error":"Ruta no existente"})
    
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci= int(self.path.split("/")[-1])
            data= self.read_data()
            pacientes = PacienteService.update_paciente(ci, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error":"Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error":"Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith == "/pacientes/":
            ci= int(self.path.split("/")[-1])
            pacientes = PacienteService.delete_paciente(ci)
            HTTPResponseHandler.handle_response(self, 200, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, PacienteRequestHandler)
        print(f" Dale !!!! Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()