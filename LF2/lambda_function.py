import json
import boto3
import logging

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


def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('lex-runtime')
    client_response = client.post_text(
    botName='photobot',
    botAlias='photobot',
    userId='serach-photos',
    inputText="show me banana")
    slots = client_response['slots']
    if slots:
        result = []
        firstslot = slots['photoslot']
        secondslot = slots['Additionalslot']
        logger.debug(firstslot)
        logger.debug(secondslot)
        for slot in slots:
            if slot is not None:
                search_data = es.search(index="photos", body={"query": {"match": {"labels": slot}}})
                result.append(search_data)
        logger.debug("ES return")
        logger.debug(serach_data)
        
    else:
        logger.debug("hello, lex is so stupid that it couldn't recognize the intents!!!")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
