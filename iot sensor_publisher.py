import time
import json
import random
import os
from dotenv import load_dotenv
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

load_dotenv()
endpoint = os.getenv('AWS_IOT_ENDPOINT', 'your-iot-endpoint.iot.us-east-1.amazonaws.com')
cert_path = os.getenv('AWS_CERT_PATH', 'certificate.pem.crt')
key_path = os.getenv('AWS_KEY_PATH', 'private.pem.key')
ca_path = os.getenv('AWS_CA_PATH', 'AmazonRootCA1.pem')

myMQTTClient = AWSIoTMQTTClient("ecosense-sensor-1")
myMQTTClient.configureEndpoint(endpoint)
myMQTTClient.configureCredentials(ca_path, key_path, cert_path)

try:
    myMQTTClient.connect()
    print("Connected to AWS IoT")
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

# Retry logic (from first doc)
retries = 3
delay = 5

while True:
    for attempt in range(retries):
        try:
            payload = {
                "timestamp": time.time(),
                "co2": random.randint(300, 800),  # Mock; uncomment for real sensors
                "temp": round(random.uniform(20, 30), 2)
            }
            # For real hardware: Uncomment Adafruit DHT22 for temperature; add MQ-135 for CO2.
            # import adafruit_dht
            # dht_device = adafruit_dht.DHT22(board.D4)
            # payload['temp'] = dht_device.temperature
            # payload['co2'] = ... # MQ-135 logic
            message = json.dumps(payload)
            myMQTTClient.publish("env/data", message, 1)  # Changed topic to match first doc
            print(f"Published: {message}")
            break
        except Exception as e:
            print(f"Publish failed (attempt {attempt+1}): {e}")
            time.sleep(delay)
    time.sleep(60)  # Every 60s