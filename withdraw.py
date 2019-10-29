from api import API
from utils import pprint, rand 

email = 'dmitry@liveplanet.net'
password = ''

api = API('studio.snb', verbose=True)

user = api.user('auth', {
    'email': email,
    'password': password,
    }
)

# user = api.user('get', {})
# print(user)

amount = 20
address = '0xcdd8fa31af8475574b8909f135d510579a8087d3'

transfer = api.user('start_withdraw', { 'amount': amount, 'address': address })
print(transfer)

pin = input("enter pin code:")
print(pin)

pprint(
    api.user('end_withdraw', {
        'pin': pin,
        'transfer_id': transfer.get('transfer_id'),
    })
)



