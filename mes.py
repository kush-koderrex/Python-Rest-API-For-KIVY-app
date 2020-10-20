from twilio.rest import Client


account_sid = 'ACef887072ea04407898c890df683a6ae7'
auth_token = '3050d33ad298b47667e21941430b2d9a'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         # media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
         from_='whatsapp:+918979266654',
         body="It's taco time!",
         to='whatsapp:+918979266654'
     )

print(message.sid)