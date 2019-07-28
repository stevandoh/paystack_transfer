from django.shortcuts import render

from .forms import CreateRecipientForm,  UpdateRecipientForm, CreateTransferForm
from django.shortcuts import render
from django.conf import settings
from .request_util import get_all_recipients, get_recipient_endpoint, set_header, get_balance_endpoint,\
    get_transfer_endpoint, get_all_recipients_by_id
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
import requests
from django.contrib import messages

headers = set_header()
balance_endpoint = get_balance_endpoint()
transfer_endpoint = get_transfer_endpoint()
recipient_endpoint = get_recipient_endpoint()
response = requests.get(balance_endpoint, headers=headers)


def home(request):
    # headers = set_header()
    # balance_endpoint = get_balance_endpoint()
    # transfer_endpoint = get_transfer_endpoint()
    response = requests.get(balance_endpoint, headers=headers)
    transfer_response = requests.get(
        transfer_endpoint, headers=headers)

    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 404:
        print('Not Found.')
    balance_request = response.json()
    transfer_request = transfer_response.json()
    data = balance_request['data']
    transfer_data = transfer_request['data']
    trial = get_all_recipients()

    # amount = balance_request['balance']
    # currency = balance_request['currency']

    return render(request, 'core/home.html', {
        'message': balance_request['message'],
        'balance': data[0]['balance'],
        'currency': data[0]['currency'],
        'data': transfer_data,
        'trial': trial


    })


def get_recipients(request):

    result = {}

    response = requests.get(recipient_endpoint, headers=headers)

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
        'data': result['data'],

    })


def create_recipient(request):
    form = CreateRecipientForm(request.POST)
    result = ''
    if form.is_valid():

        status = form.save_recipient()['status']
        if status:
            return redirect('suppliers')
        else:
            result += form.save_recipient()['message']
            return render(request, 'core/recipient_form.html', {'form': form, 'result': result})
    else:
        form = CreateRecipientForm()
    return render(request, 'core/recipient_form.html', {'form': form, 'result': result})


def update_recipient(request, id):

    form = UpdateRecipientForm(request.POST)

    result = ''

    if form.is_valid():
        result += form.update_recipient(id)['message']
        status = form.update_recipient(id)['status']
        if status:
            return redirect('suppliers')
        else:
            return render(request, 'core/edit_recipient.html', {'form': form, 'result': result})
    else:
        form = UpdateRecipientForm()
    return render(request, 'core/edit_recipient.html', {'form': form,
                                                        'result': result})


def create_transfer(request):
    form = CreateTransferForm(request.POST)

    result = ''
    if form.is_valid():

        status = form.save_transfer()['status']
        if status:
            return redirect('home')
        else:
            result += form.save_transfer()['message']
            return render(request, 'core/transfer_form.html', {'form': form, 'result': result})
    else:
        form = CreateTransferForm()
    return render(request, 'core/transfer_form.html', {'form': form, 'result': result})


def delete_recipient(request, id):

    result = ''
    delete_response = {}

    if request.method == "POST":
        response = requests.delete(
            '%s/%s' % (recipient_endpoint, id), headers=headers)

        delete_response = response.json()
        print(delete_response)
        if delete_response['status']:
            messages.success(request, "Supplier successfully deleted!")
            return redirect('suppliers')
        else:
            result += delete_response['message']
            return render(request, 'core/transfer_form.html', {'result': result})

    # context = {'movie': movie,
    #            'creator': creator,
    #            }

    return render(request, 'core/delete_recipient.html', {'data': delete_response})
# headers = {
#     'Authorization': 'Bearer sk_test_a362e380363bea61d841910010001d410bac1274',
#     'Content-Type': 'application/json',
# }

# response = requests.delete(
#     'https://api.paystack.co/transferrecipient/2295004', headers=headers)
