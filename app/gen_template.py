"""Template for task generator."""
from abc import ABCMeta, abstractmethod
import os
import hashlib
import base64
import json
from typing import Any, Dict
import random

import pika


class TaskGenTemplate(metaclass=ABCMeta):
    """Template class for task generator.

    Args:
        metaclass ([type], optional): Defaults to ABCMeta.
    """

    def __init__(self, name):
        """Basic configs."""
        self.__name__ = name
        self.__task_id__ = get_generator_id()

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(**get_connection_data()))

        self.channel = connection.channel()

        self.channel.exchange_declare(exchange='main',
                                      exchange_type='topic')

        result = self.channel.queue_declare(queue='', exclusive=False)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange='main',
                                routing_key="broadcast",
                                queue=queue_name)
        self.channel.queue_bind(exchange='main',
                                routing_key=self.__task_id__,
                                queue=queue_name)

        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.__parse, auto_ack=True)

    @abstractmethod
    def generate(self) -> Dict[str, Any]:
        """Generate task.

        Returns:
            Dict[str, Any]: task
        """

    @abstractmethod
    def whoami(self):
        """Give name and description.

        Returns:
            str: name and description of task
        """

    def listen(self):
        """Wait for requests from the control module."""
        self.channel.start_consuming()

    def __answer(self, msg: str):
        """Send answer to the control module.

        Args:
            msg (str): answer
        """
        self.channel.basic_publish(
            exchange='main', routing_key='answer', body=msg)

    def __parse(self, ch, method, properties, body: bytes):
        """Parse consumed message.

        Callback function for RabbitMQ consumed messages.

        Args:
            ch ([type]): [description]
            method ([type]): [description]
            properties ([type]): [description]
            body (bytes): Message in binary format
        """
        input_msg = body.decode()
        request = json.loads(input_msg)
        answer_msg = {}
        err_code = 0
        err_msg = ""
        req_id = request.get("id")
        try:
            tag = request["tag"]
            if tag == "who_are_you":
                answer_msg = self.whoami()
            elif tag == "task":
                answer_msg = self.generate()
            else:
                err_code = -2
                err_msg = "Unexpected param"
        except KeyError:
            err_code = -1
            err_msg = "Error request parsing"
        finally:
            self.__answer(json.dumps({"req_id": req_id,
                                      "data": answer_msg,
                                      "err": {"code": err_code,
                                              "msg": err_msg}}))


def get_generator_id() -> str:
    """Return generator ID.

    Get Generator id as base-64 encoded sha224-hash of concatenation
    os.name and PID

    Returns:
        str: generator ID
    """
    res = os.name + str(os.getpid()) + str(random.randint(-1000, 1000))
    res = hashlib.sha224(res.encode('utf-8')).digest()
    res = base64.b64encode(res).decode('utf-8')
    return res


def get_connection_data() -> Dict[str, Any]:
    """Get data to connect to RabbitMQ.

    Returns:
        Dict[str, Any]: RabbitMQ connection data
    """
    conn_info = {
        "host": os.environ["HOST"],
        "port": os.environ["PORT"]
    }
    return conn_info
