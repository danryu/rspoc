import json
import datetime

def lambda_handler(event, context):

    time = datetime.datetime.now()

    return {
        'statusCode': 200,
        'body': json.dumps("The time is now " + str(time))
    }
