import requests
from django.conf import settings


BASE_API = 'https://api.paystack.co/'
RECIPIENT_ENDPOINT = 'transferrecipient'
TRANSFER_ENDPOINT = 'transfer'
BALANCE_ENDPOINT = 'balance'


def get_recipient_endpoint():
    return '%s%s' % (BASE_API, RECIPIENT_ENDPOINT)


def get_transfer_endpoint():
    return '%s%s' % (BASE_API, TRANSFER_ENDPOINT)


def get_balance_endpoint():
    return '%s%s' % (BASE_API, BALANCE_ENDPOINT)


def set_header():
    header = {}
    header['Authorization'] = "Bearer %s" % (settings.PAYSTACK_SECRET_KEY)
    return header
    # : "Bearer %s" % (settings.PAYSTACK_SECRET_KEY), }


def get_all_recipients():

    result = {}
    key_value = {}
    url = get_recipient_endpoint()
    headers = set_header()

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print('success')
        result = response.json()
        data = result['data']
        for datum in data:
            key_value['%s (%s-%s)' % (
                datum['name'], datum['details']['account_number'], datum['details']['bank_name'])] = datum['recipient_code']

    else:
        print('error')

    return key_value


def get_recipient_by_id():

    result = {}
    key_value = {}
    url = get_recipient_endpoint()
    headers = set_header()

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print('success')
        result = response.json()
        data = result['data']
        for datum in data:
            key_value[datum['id']] = datum['recipient_code']

    else:
        print('error')

    return key_value


def get_all_recipients_by_id():

    result = {}
    key_value = {}
    url = get_recipient_endpoint()
    headers = set_header()
    #  {
    #     'Authorization': "Bearer %s" % (settings.PAYSTACK_SECRET_KEY), }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print('success')
        result = response.json()
        data = result['data']
        # key_value = data
        # name = item['name']
        # new_dict[name] = item
        for datum in data:
            # dicts[i] = values[i]
            key_value['%s' % (datum['id'])
                      ] = {'name': datum['name'],
                           'account_number': datum['details']['account_number'],
                           'bank_name': datum['details']['bank_name']}
            #  {'%s (%s-%s)' % (
            # datum['name'], datum['details']['account_number'], datum['details']['bank_name']), datum['id']}
            # name = '%s (%s)' % (datum.name, datum.account_number)
            # key_value[name] = datum.id

    else:
        print('error')

    return key_value


def get_balance():
    response = requests.get(get_balance_endpoint(), headers=set_header())
    balance_request = response.json()
    data = balance_request['data']
    return data[0]['balance']


# print(get_recipient_endpoint())
# print(get_transfer_endpoint())
print(get_balance())
balance = int(get_balance()) - 50
print(balance)
print(get_all_recipients())
