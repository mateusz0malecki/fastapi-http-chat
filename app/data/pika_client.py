import pika
import json


class PikaClient:
    def __init__(self, host):
        self.host = host
        self.connection = None
        self.channel = None
        self.queue_name = None
        self.message = None
        self.msg_list = []

    def setup(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, heartbeat=0)
        )
        self.channel = self.connection.channel()

    def publish_msg(self, message):
        self.message = message
        self.queue_name = (
            f"{self.message['user_name']}.{self.message['message']['user']}"
        )
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_publish(
            exchange="", routing_key=self.queue_name, body=json.dumps(self.message)
        )

    def receive_msg(self, queue_name):
        self.queue_name = queue_name
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.msg_list.clear()
        while True:
            method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
            if method_frame:
                body_json = json.loads(body)
                msg = f'{body_json["user_name"]}: {body_json["message"]["message"]}'
                self.msg_list.append(msg)
                self.channel.basic_ack(method_frame.delivery_tag)
            else:
                print("No message returned")
                break

    def close(self):
        self.channel.close()
        self.connection.close()
