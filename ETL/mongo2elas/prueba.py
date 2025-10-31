from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

indices = es.cat.indices(format="json")
for idx in indices:
    print(f"{idx['index']} → {idx['docs.count']} documentos")