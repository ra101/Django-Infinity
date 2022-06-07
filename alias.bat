: Python Aliases
doskey pir=pip install -r requirements.txt

:: Django Aliases
doskey dj=python manage.py $*
doskey djt=python manage.py test $*
doskey djr=python manage.py runserver $*
doskey djs=python manage.py shell $*
doskey djmm=python manage.py makemigrations $*
doskey djm=python manage.py migrate $*
doskey djcs=python manage.py collectstatic --noinput $*

doskey run_beat=celery -A infinity beat -l info $*
doskey run_celery=celery -A infinity worker -Q default_queue -P gevent -l info $*
