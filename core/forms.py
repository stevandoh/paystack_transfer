from django import forms
import requests
from .request_util import get_all_recipients, get_recipient_endpoint, get_balance_endpoint,\
    set_header, get_transfer_endpoint, get_all_recipients_by_id
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
import json


headers = set_header()
balance_endpoint = get_balance_endpoint()
transfer_endpoint = get_transfer_endpoint()
recipient_endpoint = get_recipient_endpoint()
response = requests.get(balance_endpoint, headers=headers)


class CreateRecipientForm(forms.Form):
    # text_input = forms.CharField()
    name = forms.CharField(label='The supplier name',
                           max_length=100, required=True)
    description = forms.CharField(
        label='description', max_length=100, help_text='service provided by the supplier')
    account_number = forms.CharField(
        label='account number', max_length=20, min_length=10, required=True)

    bank_name = forms.CharField(
        label='Bank name', max_length=50, initial='Access Bank')

    currency = forms.CharField(
        label='Currency', max_length=3, initial='NGN', disabled=True)

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('text_input', css_class='input-xlarge'),
        FormActions(
            Submit('save_changes', 'Save', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )

    def save_recipient(self):

        result = ''

        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        account_number = self.cleaned_data['account_number']
        # bank_name = self.cleaned_data['bank_name']
        # currency = self.cleaned_data['currency']

        payload = {
            "type": "nuban",
            "name": name,
            "description": description,
            "account_number": account_number,
            "bank_code": "044",
            "currency": "NGN",
        }

        # response = requests.get(url, headers=headers)

        data = json.dumps(payload)

        response = requests.post(
            recipient_endpoint, headers=headers, data=data)

        print(response.json())
        result = response.text
        print(json.loads(result))
        print(response.status_code)

        if response.status_code == 200:  # SUCCESS
            result = response.json()
            print("other reuslt",  result)

        return json.loads(result)


class UpdateRecipientForm(forms.Form):
    # text_input = forms.CharField()

    name = forms.CharField(label='The supplier name',
                           max_length=100, required=True,)
    description = forms.CharField(
        label='description', max_length=100, help_text='service provided by the supplier', required=False)
    # account_number = forms.CharField(
    #     label='account number', max_length=20, min_length=10, required=False)

    # bank_name = forms.CharField(
    #     label='Bank name', max_length=50, initial='Access Bank')

    # currency = forms.CharField(
    #     label='Currency', max_length=3, initial='NGN')

    def update_recipient(self, id):

        result = ''

        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        # account_number = self.cleaned_data['account_number']
        # bank_name = self.cleaned_data['bank_name']
        # currency = self.cleaned_data['currency']

        payload = {
            "type": "nuban",
            "name": name,
            "description": description,
            # "account_number": account_number,
            "bank_code": "044",
            "currency": "NGN",
        }

        # response = requests.get(url, headers=headers)

        data = json.dumps(payload)

        response = requests.put(
            '%s/%s' % (recipient_endpoint, id), headers=headers, data=data)

        print(response.json())
        result = response.text
        print(json.loads(result))
        print(response.status_code)

        if response.status_code == 200:  # SUCCESS
            # result = response.json()
            print("other reuslt",  response.json())

        return json.loads(result)


class CreateTransferForm(forms.Form):

    recipients = get_all_recipients()
    # balance

    # source, amount, currency, reason, recipient
    # text_input = forms.CharField()

    RECIPIENT_CHOICES = [
        tuple([x, x]) for x in [k for k in recipients]
    ]

    reason = forms.CharField(
        label='Reason', max_length=100, help_text='reason of the payment')
    amount = forms.IntegerField(
        label='Amount', max_value=1000000, min_value=100, required=True, help_text='Minimum transfer amount is NGN 100')

    currency = forms.CharField(
        label='Currency', max_length=3, initial='NGN', disabled=True)

    if len(RECIPIENT_CHOICES) > 0:

        recipient = forms.CharField(
            label='Select the supplier', widget=forms.Select(choices=RECIPIENT_CHOICES))
    # else:

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('text_input', css_class='input-xlarge'),
        FormActions(
            Submit('save_changes', 'Save', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )

    def save_transfer(self):

        result = ''

        reason = self.cleaned_data['reason']
        amount = self.cleaned_data['amount']
        recipient_detail = self.cleaned_data['recipient']

        recipients = get_all_recipients()

        payload = {
            "source": "balance",
            "amount": amount,
            "reason": reason,
            "recipient": recipients[recipient_detail],
        }

        # response = requests.get(url, headers=headers)

        data = json.dumps(payload)

        response = requests.post(
            transfer_endpoint, headers=headers, data=data)

        print(response.json())
        result = response.text
        print(json.loads(result))
        print(response.status_code)

        if response.status_code == 200:  # SUCCESS
            # result = response.json()
            print("other reuslt",  result)

        return json.loads(result)
