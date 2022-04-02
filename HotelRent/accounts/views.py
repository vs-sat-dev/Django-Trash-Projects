from django.shortcuts import render
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
import six

from.forms import RegisterForm


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print('Form1 response ', form.data['username'])
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Verify your email address'
            message = render_to_string('email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            print('Message check ', message)
            print('Id check ', user.id)
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'please-confirm-email.html')
        else:
            context = {'errors': form.errors, 'form': form}
            return render(request, 'register.html', context=context)
    else:
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context=context)


def email_activation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        print('UID check ', uid)
    except Exception as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        context = {'message': 'Thank you for your email confirmation. Now you can login your account.'}
        return render(request, 'email-activation.html', context=context)
    else:
        context = {'message': 'Activation link is invalid!'}
        return render(request, 'email-activation.html', context=context)
