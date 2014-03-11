from cdf.metadata.url import ELASTICSEARCH_BACKEND

# By default, when tasks pull files from s3, local files are ignored
DEFAULT_FORCE_FETCH = True

# ElasticSearch mapping, for creating a new index
ES_MAPPING = ELASTICSEARCH_BACKEND.mapping()