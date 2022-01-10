import json
import yfinance as yf
from datetime import datetime

def lambda_handler(event, context):

    print(event)
    paper = event['pathParameters']['stock']

    try:
        price = yf.Ticker(f'{paper.upper()}.SA').history(period='1m', interval='1m')['Close'][0]
        print(price)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'stock': 'WEGE3',
                'price': float(price),
                'timestamp': datetime.now().isoformat()
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': f'Paper {paper} not found.'
            })
        }
