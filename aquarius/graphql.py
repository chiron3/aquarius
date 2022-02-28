import logging
import time

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.aiohttp import log as aiohttp_logger

from aquarius.events.util import get_network_name

logger = logging.getLogger("aquarius")
aiohttp_logger.setLevel(logging.WARNING)


def get_number_orders(token_address, last_sync_block):
    try:
        client = get_client()

        last_block = get_last_block(client)
        while last_block < last_sync_block:
            last_block = get_last_block(client)
            time.sleep(2)

        did_query = gql('{ nft(id: "' + token_address.lower() + '") { orderCount } }')
        result = client.execute(did_query)

        return int(result["nft"]["orderCount"])
    except Exception:
        logger.error(
            f"Can not get number of orders for subgraph {get_network_name()} token address {token_address}"
        )
        return -1


def get_transport():
    network_name = get_network_name()
    if network_name == "development":
        prefix = "http://localhost:9000"
    else:
        prefix = f"http://v4.subgraph.{network_name}.oceanprotocol.com"

    return AIOHTTPTransport(url=f"{prefix}/subgraphs/name/oceanprotocol/ocean-subgraph")


def get_client():
    return Client(transport=get_transport(), fetch_schema_from_transport=True)


def get_last_block(client):
    last_block_query = gql("{_meta { block { number } } }")

    try:
        result = client.execute(last_block_query)
        last_block = result["_meta"]["block"]["number"]
    except (KeyError, IndexError):
        raise IndexError(
            "Can not get last block name for subgraph {get_network_name()}"
        )

    return last_block