import json
import pytest
import pika
from app.routers.rabbitmq import publish_client

class DummyChannel:
    def __init__(self):
        self.published = []
    def exchange_declare(self, exchange, exchange_type, durable):
        # on ne fait rien, juste on simule
        pass
    def basic_publish(self, exchange, routing_key, body, properties):
        # on stocke pour vérification
        self.published.append((exchange, routing_key, body, properties))

class DummyConnection:
    def __init__(self):
        self._channel = DummyChannel()
    def channel(self):
        return self._channel
    def close(self):
        # on peut marquer la fermeture si besoin
        self.closed = True

@pytest.fixture
def dummy_conn(monkeypatch):
    """
    Monkey-patch pika.BlockingConnection pour toujours
    retourner la même DummyConnection.
    """
    conn = DummyConnection()
    monkeypatch.setattr(pika, "BlockingConnection", lambda params: conn)
    return conn

def test_publish_client(dummy_conn):
    # Données factices à publier
    client_data = {"id": 1, "name": "ordi", "price": 5}

    # Appel de la fonction à tester
    publish_client(client_data)

    # Récupère le channel et sa liste de messages
    channel = dummy_conn.channel()
    assert channel.published, "Aucun message n'a été publié"

    exchange, routing_key, body, props = channel.published[0]

    # Vérifications
    assert exchange == "produits"
    assert routing_key == ""
    assert json.loads(body) == client_data
    assert props.content_type == "application/json"