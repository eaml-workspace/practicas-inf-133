from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

pacientes={}

class Paciente:
    def __init__(self):
        self.ci = None
        self.nombre = None
        self.apellido = None
        self.edad = None
        self.diagnostico = None
        self.genero = None
        self.doctor = None
    
    def __str__(self):
        return f"Ci: {self.ci}, Nombre: {self.nombre}, Apellido: {self.apellido}, Edad: {self.edad}, Género: {self.genero}, Diagnostico: {self.diagnostico}, Doctor: {self.doctor}"

class PacienteBuilder:
    def __init__(self):
        self.paciente = Paciente()
    
    def set_ci(self, ci):
        self.paciente.ci = ci
    
    def set_ci(self, nombre):
        self.paciente.nombre = nombre
    
    def set_apellido(self, apellido):
        self.paciente.apellido = apellido
    
    def set_edad(self, edad):
        self.paciente.edad = edad
    
    def set_genero(self, genero):
        self.paciente.genero = genero
    
    def set_diagnostico(self, diagnostico):
        self.paciente.diagnostico = diagnostico
    
    def set_doctor(self, doctor):
        self.paciente.doctor = doctor
    
    def get_paciente(self):
        return self.paciente

class Hospital:
    def __init__(self, builder):
        self.builder = builder
    
    def create_paciente(self, ci, nombre, apellido, edad, genero, diagnostico, doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        return self.builder.get_paciente()

############################## VERIFICAR ##################################

class PacienteService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.hospital = Hospital(self.builder)
    
    def add_paciente(self, post_data):
        ci = post_data.get("ci", None)
        nombre = post_data.get("nombre", None)
        apellido = post_data.get("apellido", None)
        genero = post_data.get("genero", None)
        edad = post_data.get("edad", None)
        diagnostico = post_data.get("diagnostico", None)
        doctor = post_data.get("doctor", None)
        
        paciente = self.hospital.create_paciente(ci, nombre, apellido, edad, genero, diagnostico, doctor)
        pacientes[len(pacientes)+1]=paciente
        return paciente
    ### cambiar.... ci como index########
    def read_pacientes(self):
        return {index: paciente.__dict__ for index, paciente in pacientes.items()}
    
    def update_paciente(self,index,data):
        if index in pacientes:
            paciente = pacientes[index]
            ##ci = data.get("ci", None)
            nombre = data.get("nombre", None)
            apellido = data.get("apellido", None)
            genero = data.get("genero", None)
            edad = data.get("edad", None)
            diagnostico = data.get("diagnostico", None)
            doctor = data.get("doctor", None)
            #if ci:
            #    paciente.ci= ci
            if nombre:
                paciente.nombre= nombre
            if apellido:
                paciente.apellido= apellido
            if edad:
                paciente.edad= edad
            if diagnostico:
                paciente.diagnostico= diagnostico
            if genero:
                paciente.genero= genero
            if doctor:
                paciente.doctor= doctor
            
            return paciente
        else:
            return None 
    
    def delete_paciente(self, index):
        if index in pacientes:
            return pacientes.pop(index)
        else:
            return None
    
    def find_paciente_ci(ci):
        return {index: paciente.__dict__ for index, paciente in pacientes.items() if paciente["ci"] == ci}
    
    def find_paciente_diagnostico(diagnostico):
        """pac=[]
        for paciente in pacientes:
            if paciente["diagnostico"] == diagnostico:
                pac.append(paciente)"""
        return {index: paciente.__dict__ for index, paciente in pacientes.items() if paciente["diagnostico"] == diagnostico}
    
    def find_paciente_doctor(doctor):
        return {index: paciente.__dict__ for index, paciente in pacientes.items() if paciente["doctor"] == doctor}
    


class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller= PacienteService
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        if self.path == "/pacientes":
            data = self.handle_reader()
            pacientes = PacienteService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error":"Ruta no existente"})
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if self.path == "/pacientes":
            response_data = self.controller.read_pacientes(self)
            HTTPResponseHandler.handle_response(self, 200, response_data)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
        
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
            ci= int(self.path.split("/")[2])
            delete_paciente = self.controller.delete_paciente(ci)
            if delete_paciente:
                HTTPResponseHandler.handle_reader(self, 200, {"message": "Paciente eliminado"})
            else:
                HTTPResponseHandler.handle_reader(self, 404, {"Error": "CI no válido"})
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, PacienteHandler)
        print(f" Dale !!!! Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()