import time
import board
import adafruit_dht
import requests
import json

url = "http://52.23.188.230:8000"

payload = {
  'username': 'began',
  'password': 'Bredpit1065'
}

files=[]
header={}
response = requests.request("POST", f'{url}/api/account/login', headers=header, data=payload, files=files)
rps = response.text

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

pKey = dtk["data"]["public_key"]

print(pKey)

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

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

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
