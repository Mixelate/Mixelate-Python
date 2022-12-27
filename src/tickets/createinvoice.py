import yaml
import paypalrestsdk
from paypalrestsdk import Invoice

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

paypal_client_id = data["PayPal"]["PAYPAL_CLIENT_ID"]
paypal_client_secret = data["PayPal"]["PAYPAL_CLIENT_SECRET"]

my_api = paypalrestsdk.Api({
  'mode': 'live',
  'client_id': paypal_client_id,
  'client_secret': paypal_client_secret})

async def createinvoice(total, channel_id):
    invoice = Invoice({
        "merchant_info": {
            "business_name": "PrismStudios",
        },
        "items": [
            {
                "name": "Commission",
                "quantity": 1,
                "unit_price": {
                    "currency": "USD",
                    "value": total
                }
            }
        ],
        "note": f"An order processed in the PrismStudios Discord server. ({channel_id})",
        "payment_term": {
            "term_type": "NET_45"
        }
    }, api=my_api)

    if invoice.create():
        invoice = Invoice.find(invoice['id'], api=my_api)
        if invoice.send():
            id = invoice.id
            return(id)