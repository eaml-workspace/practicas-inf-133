from zeep import Client

client = Client('http://localhost:8000')

result = client.service.SumaDosNumeros(numero1=10, numero2=2)
print(result)

result = client.service.RestaDosNumeros(numero1=10, numero2=2)
print(result)

result = client.service.MultiplicacionDosNumeros(numero1=10, numero2=2)
print(result)

result = client.service.DivisionDosNumeros(numero1=10, numero2=2)
print(result)
