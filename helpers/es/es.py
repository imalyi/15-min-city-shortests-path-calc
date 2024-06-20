# This script create addresses collection for searching addresses.

from opensearchpy import OpenSearch
import json
from opensearchpy.helpers import bulk
from database import MongoDatabase
from config import OPENSEARCH_PORT, OPENSEARCH_HOST, OPENSEARCH_PASSWORD, OPENSEARCH_USER

index_name = 'addresses'

opensearch = OpenSearch(
    hosts = [{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    http_auth = (OPENSEARCH_USER, OPENSEARCH_PASSWORD),
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
)

def save_addresses_from_mongo_to_json():
    m = MongoDatabase()
    addresses = []
    for poi in m.get_all_pois():
        addresses.append(poi.get('address').get('full'))
    with open('addresses.json', 'w') as f:
        f.write(json.dumps(addresses, ensure_ascii=False))

def create_index_if_not_exists():
    if not opensearch.indices.exists(index=index_name):
        opensearch.indices.create(index=index_name)

def read_addresses() -> list[str]:
    with open('addresses.json', 'r') as file:
        addresses = json.load(file)
    return addresses

def clean_address_index():
    query_body = {
        "query": {
            "match_all": {}  # Match all documents
        }
    }
    response = opensearch.delete_by_query(index=index_name, body=query_body)
    return response

def insert_addresses():
    clean_address_index()
    actions = []
    for address in read_addresses():
        actions.append({
            "_index": index_name,
            "_source": {'full': address}
        })

    bulk(opensearch, actions)
    print("Addresses indexed successfully.")

def fuzzy_search(query) -> list[str]:
    opensearch = OpenSearch(
    hosts = [{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    http_auth = (OPENSEARCH_USER, OPENSEARCH_PASSWORD),
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    )

    query_body = {
        "query": {
            "fuzzy": {
                "full": {
                    "value": query,
                    "fuzziness": 50
                }
            }
        }
    }
    result = opensearch.search(index=index_name, body=query_body)
    return [hit['_source']['full'] for hit in result['hits']['hits']][:5]


def create_es():
    #save_addresses_from_mongo_to_json()
  #  clean_address_index()
  #  create_index_if_not_exists()
    insert_addresses()


create_es()
