from zeep import Client

def call_wsdl_service(wsdl_url, operation, **kwargs):
    client = Client(wsdl_url)
    response = getattr(client.service, operation)(**kwargs)
    return response
