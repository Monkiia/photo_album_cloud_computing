import json
import logging
import boto3
from elasearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
esEndpoint = "https://vpc-photos-hj63c4poxaxhbts42tlxej3hyu.us-east-1.es.amazonaws.com"

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

es = Elasticsearch(
    hosts=[{'host': esEndPoint, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

def lambda_handler(event, context):
    # TODO implement

    logger.debug(event);
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
