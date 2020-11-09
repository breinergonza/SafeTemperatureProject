import time
import board
import adafruit_dht
import requests
import json
from io import open
import binascii

from datetime import datetime

# from Crypto.PublicKey import DSA
# from Crypto.Cipher import AES, PKCS1_OAEP
# from Crypto.Hash import SHA256
# from Crypto.Signature import DSS

url = "http://52.23.188.230:8000"
payload = {
   'username': 'breinergonza',
   'password': 'Bredpit1065'
 }

files=[]
header={}
response = requests.request("POST", f'{url}/api/account/login', headers=header, data=payload, files=files)
rps = response.text

print(rps)

# login = json.dumps(rps)
dt = json.loads(rps)

token = dt["token"]

print(token)

header={
        'Authorization': f'Token {token}'
    }

respKey = requests.request("GET", f'{url}/gKeyDsa', headers=header, data=payload)
rpsKey = respKey.text

dtk = json.loads(rpsKey)

pKey = dtk["data"]["private_key"]

print(pKey)

signature = bytes.fromhex(pKey)

# Se inhabilita porque el procesado no soporta DSA
#Obtengo y guardo la llave privada para cifrar los datos
# file_out = open("./archivos/private_key_dsa.pem", "wb")
# file_out.write(signature)
# file_out.close()


class Switcher(object):
    def numbers_to_seg(self, argument):
        """Dispatch method"""
        method_name = 'seg_' + str(argument)
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid second")
        return method()
 
    def seg_5(self):

        return "min_5"
 
    def seg_15(self):

        return "min_15"
 
    def seg_25(self):

        return "min_25"
    
    def seg_35(self):

        return "min_35"
    
    def seg_45(self):

        return "min_45"
    
    def seg_55(self):

        return "min_55"

# Conexión al sensor
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)


while True:
    
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        
        temperatura = f'{temperature_c}'

# Aqui es donde firmaba la información, se retira para firmarla con el API
#         hash_obj = SHA256.new(temperatura.encode("utf8"))
#         key = DSA.import_key(open("./archivos/private_key_dsa.pem").read())
#         signer = DSS.new(key, 'fips-186-3')
#         signature = signer.sign(hash_obj)
#         dts = binascii.hexlify(signature).decode('utf8')

        urlCifrarTemp = f'{url}/codeTxt/'

        payloadCifrarTemp={
            'texto': temperatura
            }
        
        pCt = json.dumps(payloadCifrarTemp)

        print(pCt)

        headersCifrarTemp = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }

        responseCifrarTemp = requests.request("POST", urlCifrarTemp, headers=headersCifrarTemp, data=pCt)
        print(responseCifrarTemp.text)
        
        ky = json.loads(responseCifrarTemp.text)

        dts = ky["firma"]

        print("Datos cifrado : " + dts)    

        i = 1

        while True:
            time.sleep(1.0)
            now = datetime.now()
            seg = f'{now.second}'
            newstr = seg[-1:]
            if newstr=="5":            
                break
            else:
                i = i + 1        
        
        a=Switcher()
        respSeg = a.numbers_to_seg(now.second)
        
        print(respSeg)

        urlGrafica = f'{url}/vTemp/'

        payloadGrafica={
            'minuto': respSeg,
            'temperatura': temperatura,
            'firma': dts
            }
        
        pGr = json.dumps(payloadGrafica)

        print(pGr)

        headersGrafica = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }

        responseGrafica = requests.request("POST", urlGrafica, headers=headersGrafica, data=pGr)
        print(responseGrafica.text)


    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(5.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(5.0)
