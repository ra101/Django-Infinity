# Python Aliases
alias pir='pip install -r requirements.txt'

## Django Aliases
dj() { command python manage.py $*;}
alias djt='python manage.py test'
alias djr='python manage.py runserver'
alias djs='python manage.py shell'
alias djmm='python manage.py makemigrations'
alias djm='python manage.py migrate'
alias djcs='python manage.py collectstatic --noinput --clear'
