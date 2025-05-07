# rca_sdk/plugins/logs/elk.py

from elasticsearch import Elasticsearch

def get_logs(timestamp, config):
    es_conf = config["elasticsearch"]

    es = Elasticsearch(
        es_conf["host"],
        basic_auth=(es_conf["username"], es_conf["password"]),
        verify_certs=es_conf.get("use_ssl", False)
    )

    # Build query: fetch logs from ±15 minutes of timestamp
    query = {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": f"{timestamp}||-15m",
                    "lte": f"{timestamp}||+15m"
                }
            }
        },
        "sort": [{ "@timestamp": "desc" }]
    }

    resp = es.search(index=es_conf["index"], body=query, size=100)
    return [hit["_source"] for hit in resp["hits"]["hits"]]
