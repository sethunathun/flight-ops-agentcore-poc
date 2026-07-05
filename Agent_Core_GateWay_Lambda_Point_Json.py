{
  "name": "get_flight_status",
  "description": "Look up current status of a flight by flight number",
  "inputSchema": {
    "type": "object",
    "properties": {
      "flightNumber": { "type": "string" }
    },
    "required": ["flightNumber"]
  }
}