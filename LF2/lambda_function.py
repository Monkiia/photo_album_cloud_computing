import json
import boto3
import logging
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
esEndpoint = "search-photos-po6tcso56ojpdg7fr2ebmjatoy.us-east-1.es.amazonaws.com"

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

es = Elasticsearch(
    hosts=[{'host': esEndpoint,'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

def getpaths(slots):
    result = []
    if slots:
        firstslot = slots['photoslot']
        secondslot = slots['Additionalslot']
        logger.debug(firstslot)
        logger.debug(secondslot)
        for slot in slots.values():
            if slot is not None:
                search_data = es.search(index="photos", body={"query": {"match": {"labels": slot}}})
                #result.append(search_data)
                logger.debug("ES return")
                logger.debug(search_data)
                if 'hits' in search_data:
                    for files in search_data['hits']['hits']:
                        filename = files['_source']['objectKey']
                        logger.debug(filename)
                        result.append(filename)
    return result


def lambda_handler(event, context):
    # TODO implement
    #logger.debug("SHOW SEARCH EVENT")
    #logger.debug(event['queryStringParameters'])
    logger.debug("print event")
    logger.debug(event)
    logger.debug(es.search(index="photos"))
    label = event['queryStringParameters']['label']
    client = boto3.client('lex-runtime')
    client_response = client.post_text(
    botName='photobot',
    botAlias='photobot',
    userId='serach-photos',
    inputText= label)
    slots = client_response['slots']
    result = getpaths(slots)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin' : '*'
        },
        'body': json.dumps(result)
    }
