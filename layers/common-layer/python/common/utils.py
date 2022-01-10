import json


# Decorators
def capture_value_error(fn, status_code=400):
    def inner(event, context):
        try:
            return fn(event, context)
        except ValueError as e:
            return {
                'statusCode': status_code,
                'body': json.dumps({'message': str(e)})
            }
    return inner
