from elasticsearch import Elasticsearch

# Config
ES_HOST = "http://localhost:9200"
INDEX = "rca-logs"

# Initialize Elasticsearch client
es = Elasticsearch(ES_HOST)

# Build the test query
query = {
    "query": {
        "match_all": {}
    },
    "sort": [{ "@timestamp": "desc" }],
    "size": 5
}

# Execute the query
response = es.search(index=INDEX, body=query)

# Print the results
hits = response["hits"]["hits"]

if not hits:
    print("[⚠️] No logs found.")
else:
    print(f"[✅] Found {len(hits)} log(s):\n")
    for hit in hits:
        source = hit["_source"]
        print(f"{source.get('@timestamp')} | {source.get('level', '')} | {source.get('message', '')}")
