EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD='myPassword!123' # your email password
EMAIL_HOST_USER="example@gmail.com" # your email id
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
O_AUTH_SECRET =  "secret "# your oauth secret from (omniport) information management group
DJANGO_SECRET = '%7i(0wlis0^g(fw*-)hm9z75@vq)mm0=dq5f^t0!k#5auw8jo_' # or your own django secret