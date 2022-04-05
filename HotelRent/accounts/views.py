from django.shortcuts import render, redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, urlencode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
import six

from.forms import RegisterForm, LoginForm, ProfileForm, UserForm, PasswordChangeForm
from .models import Profile, EmailConfirmation


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
        if user.is_active:
            context = {'message': 'Your email was changed successfully.'}
            email_confirmation = EmailConfirmation.objects.filter(user=user).first()
            user.email = email_confirmation.new_email
            email_confirmation.delete()
        else:
            context = {'message': 'Thank you for your email confirmation. Now you can login your account.'}
            user.is_active = True
        user.save()
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
    message = request.GET.get('message')
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    if profile:
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=user)
        password_change_form = PasswordChangeForm()
        context = {'user': user, 'profile': profile, 'user_form': user_form, 'profile_form': profile_form,
                   'password_change_form': password_change_form, 'message': message}
        return render(request, 'profile.html', context=context)


@login_required(login_url='accounts:login')
def image_change(request):
    message = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=Profile.objects.get(user=request.user))
        if form.is_valid:
            form.save()
        else:
            message = 'Invalid form'

    if message:
        return redirect(f'profile/{request.user.username}?{urlencode({"message": message})}')
    else:
        return redirect(f'profile/{request.user.username}')


@login_required(login_url='accounts:login')
def email_change(request):
    message = None
    if request.method == 'POST':
        form = UserForm(request.POST, instance=User.objects.get(username=request.user.username))
        if form.is_valid:
            if User.objects.filter(email=form.data['email']).first() is None \
              and EmailConfirmation.objects.filter(new_email=form.data['email']).first() is None:
                email_confirmation = EmailConfirmation.objects.create(user=request.user, new_email=form.data['email'])

                current_site = get_current_site(request)
                mail_subject = 'Verify your email address'
                message = render_to_string('email.html', {
                    'user': request.user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(request.user.id)),
                    'token': account_activation_token.make_token(request.user),
                })
                to_email = form.data['email']
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                print('Email was sent')
            else:
                message = 'Email already exist'
        else:
            message = 'Invalid form'

    if message:
        return redirect(f'profile/{request.user.username}?{urlencode({"message": message})}')
    else:
        return redirect(f'profile/{request.user.username}')


@login_required(login_url='accounts:login')
def password_change(request):
    message = None
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid:
            user = authenticate(username=request.user.username, password=form.data['old_password'])
            if user:
                if form.data['new_password'] == form.data['new_password_confirm']:
                    user.set_password(form.data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)
                else:
                    message = 'Passwords doesn\'t match'
            else:
                message = 'Wrong old password'

    if message:
        return redirect(f'profile/{request.user.username}?{urlencode({"message": message})}')
    else:
        return redirect(f'profile/{request.user.username}')
