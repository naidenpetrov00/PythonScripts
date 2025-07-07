from zeep import Client
from zeep.transports import Transport
from requests import Session

session = Session()
# session.cert = ('/path/to/client.crt', '/path/to/client.key')  # или .pem, .pfx
session.verify = True  # или False ако сертификатът не е trusted
transport = Transport(session=session)

client = Client(wsdl="https://edelivery.egov.bg/Services/EDeliveryIntegrationService.svc?singleWsdl", transport=transport)

for service in client.wsdl.services.values():
    for port in service.ports.values():
        operations = sorted(port.binding._operations.values(), key=lambda x: x.name)
        for operation in operations:
            print(f"{operation.name}({operation.input.signature()}) -> {operation.output.signature()}")

# Извикване на метод
# result = client.service.GetRegisteredInstitutions()
