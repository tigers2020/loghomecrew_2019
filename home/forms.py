from ckeditor.fields import RichTextFormField
from ckeditor.widgets import CKEditorWidget
from django import forms
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


def get_question_type():
    questions = (
        ('1', 'Feed Back'),
        ('2', 'General Questions'),
        ('3', 'Purchase')
    )
    return questions


class ContactForm(forms.Form):
    first_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(label='',
                             widget=forms.TextInput(attrs={'placeholder': 'E-Mail', 'class': 'form-control'}))
    subject = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Subject', 'class': 'form-control input_box'}))
    topic = forms.ChoiceField(choices=get_question_type(), label='',
                              widget=forms.Select(attrs={'class': 'mdb-select md-form colorful-select dropdown-ins'}))
    message = RichTextFormField(label='', widget=CKEditorWidget(
        attrs={'placeholder': 'Message', 'class': 'form-control'}))
    captcha = ReCaptchaField(widget=ReCaptchaWidget(), label="")

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['cols'] = 10
        self.fields['message'].widget.attrs['rows'] = 20
