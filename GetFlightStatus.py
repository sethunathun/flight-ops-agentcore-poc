import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FlightStatus')

def lambda_handler(event, context):
    flight_number = event.get('flightNumber', '').upper()
    response = table.get_item(Key={'FlightNumber': flight_number})
    item = response.get('Item')
    if not item:
        return {"result": f"No record found for flight {flight_number}"}
    return {
        "result": f"{flight_number}: {item['Status']}, Gate {item['Gate']}, departure {item['DepartureTime']}"
    }