
import random
import string
import json

def rand():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))

def pprint(obj):
    print(json.dumps(obj, indent=4))