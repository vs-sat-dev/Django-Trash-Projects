from django.shortcuts import render, redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
import six

from.forms import RegisterForm, LoginForm
from .models import Profile


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def register(request):
    if request.user.is_authenticated:
        return redirect(f'profile/{request.user.username}')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
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
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        context = {'message': 'Thank you for your email confirmation. Now you can login your account.'}
        return render(request, 'email-activation.html', context=context)
    else:
        context = {'message': 'Activation link is invalid!'}
        return render(request, 'email-activation.html', context=context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect(f'profile/{request.user.username}')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('Form data email ', form.data['email'])
            print('Form data password ', form.data['password'])
            username = User.objects.get(email=form.data['email']).username
            user = authenticate(username=username, password=form.data['password'])
            if user is not None:
                login(request, user)
                return redirect(f'profile/{username}')
            else:
                context = {'form': form, 'message': 'The email address or password is wrong.'}
                return render(request, 'login.html', context=context)
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context=context)


@login_required(login_url='accounts:login')
def logout_user(request):
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    context = {'user': user, 'profile': profile}
    return render(request, 'profile.html', context=context)


@login_required(login_url='accounts:login')
def image_change(request):
    if request.method == 'POST':
        form = request.POST
        print('Form image ', form.getlist('image'))
