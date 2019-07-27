from django import forms
import requests
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
import json


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
        label='Currency', max_length=3, initial='NGN')

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

        headers = {
            'Authorization': 'Bearer sk_test_a362e380363bea61d841910010001d410bac1274',
            'Content-Type': 'application/json',
        }

        result = ''

        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        account_number = self.cleaned_data['account_number']
        bank_name = self.cleaned_data['bank_name']
        currency = self.cleaned_data['currency']

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
            'https://api.paystack.co/transferrecipient', headers=headers, data=data)

        print(response.json())
        result = response.text
        print(json.loads(result))
        print(response.status_code)

        if response.status_code == 200:  # SUCCESS
            result = response.json()
            print("other reuslt",  result)

        return json.loads(result)
