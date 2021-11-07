import json
import logging
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

s3 = boto3.client("s3",region_name='us-east-1')
rekognition = boto3.client('rekognition',region_name='us-east-1')
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


def lambda_handler(event, context):
    # TODO implement

    logger.debug(event)
    records = event['Records']
    
    for record in records:
        s3object = record['s3']
        bucket = s3object['bucket']['name']
        object_key =s3object['object']['key']
        image = {
            'S3Object': {
                'Bucket': bucket,
                'Name': object_key
            }
        }
        metadata = s3.head_object(Bucket=bucket, Key=object_key)['Metadata']['customlabels']
        user_defined_labels = metadata.split(",")
        logger.debug("METADATA")
        logger.debug(metadata)
        #logger.debug(image)
        response = rekognition.detect_labels(Image = image)
        logger.debug(response)
        labels = list(map(lambda x:x['Name'],response['Labels']))
        combolabels = user_defined_labels + labels
        timestamp = record['eventTime']
        es_object = json.dumps({
            'objectKey' : object_key,
            'bucket' : bucket,
            'createdTimestamp' : timestamp,
            'labels' : combolabels
        })
        es.index(index="photos", doc_type="Photo", id=object_key, body=es_object, refresh=True)
        logger.debug("successful log")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambdaaa!')
    }
