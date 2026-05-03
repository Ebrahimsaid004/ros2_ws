import paho.mqtt.client as mqtt
import subprocess

BROKER = "0c841676725b4046a512c2491cd5da74.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "Mariam"
PASSWORD = "Mariam23"

TOPIC = "robot/message"

def on_connect(client, userdata, flags, rc):
    print("✅ Connected with result code:", rc)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print("📩 Received:", message)

    if message == "1":
        print("➡ open file one ")
        
        subprocess.run(["bash", "/home/ibrahim/ros2_ws/run_arm.sh"])
        


    elif message == "2":
        print("➡ open file two")
        subprocess.run(["bash", "/home/ibrahim/ros2_ws/run_arm2.sh"])

    else:
        print("❌ wrong num")
   

client = mqtt.Client()

client.username_pw_set(USERNAME, PASSWORD)

client.tls_set()  # 🔥 مهم جدًا في Cloud

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

client.subscribe(TOPIC)

print("Waiting for messages...")

client.loop_forever()
