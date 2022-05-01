from django.core.mail import send_mail


def send_confirmation_email(activation_code, email):
    full_link = f'http://localhost:8000/v1/api/client/activate/{activation_code}'

    send_mail(
        'Привет',
        full_link,
        '5kanolesya@gmail.com',
        [email]
    )