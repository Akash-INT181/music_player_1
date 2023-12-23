from elasticsearch import Elasticsearch

SONG_INDEX_NAME = "search-song-index"

ELASTICSEARCH_URL = "https://localhost:9200"
es = Elasticsearch(
    hosts=ELASTICSEARCH_URL,
    basic_auth=("elastic", "SwY+1mwboS-RWS*JwVHk"),
    verify_certs=False,
)
