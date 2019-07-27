from django.shortcuts import render

from .forms import CreateRecipientForm
from django.shortcuts import render
from django.conf import settings
import requests
from django.shortcuts import redirect
from django.http import HttpResponse


def home(request):
    headers = {
        'Authorization': 'Bearer sk_test_a362e380363bea61d841910010001d410bac1274',
    }
    response = requests.get('https://api.paystack.co/balance', headers=headers)

    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 404:
        print('Not Found.')
    balance_request = response.json()
    data = balance_request['data']

    # amount = balance_request['balance']
    # currency = balance_request['currency']

    return render(request, 'core/home.html', {
        'message': balance_request['message'],
        'balance': data[0]['balance'],
        'currency': data[0]['currency']


    })


def get_recipients(request):

    result = {}
    url = "https://api.paystack.co/transferrecipient"
    headers = {
        'Authorization': "Bearer sk_test_a362e380363bea61d841910010001d410bac1274", }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print('success')
        result = response.json()
        # result['success'] = True
    else:
        print('error')
        # result['success'] = False
        # if response.status_code == 404:
        # result['message'] = 'No entry found for "%s"' % word
        # else:
        # result['message'] = 'The Oxford API is not available at the moment. Please try again later.'
    # return result

    return render(request, 'core/recipients.html', {
        'data': result['data']
    })


def create_recipient(request):
    form = CreateRecipientForm(request.POST)
    result = ''
    if form.is_valid():
        result += form.save_recipient()['message']
        status = form.save_recipient()['status']
        if status:
            return redirect('suppliers')
        else:
            return render(request, 'core/recipient_form.html', {'form': form, 'result': result})
    else:
        form = CreateRecipientForm()
    return render(request, 'core/recipient_form.html', {'form': form, 'result': result})


# def github(request):
    # search_result = {}
    # if 'username' in request.GET:
    #     username = request.GET['username']
    #     url = 'https://api.github.com/users/%s' % username
    #     response = requests.get(url)
    #     search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
    #     search_result = response.json()
    #     search_result['success'] = search_was_successful
    #     search_result['rate'] = {
    #         'limit': response.headers['X-RateLimit-Limit'],
    #         'remaining': response.headers['X-RateLimit-Remaining'],
    #     }
    # return render(request, 'core/github.html', {'search_result': search_result})
