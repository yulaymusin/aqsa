# Aqsa
Aqsa is a personal finance software.

Aqsa is simple, but free software which have some powerful functionality even compare some commercial software.

Aqsa is made using Python 3 and Django Framework.

## Online
https://musinaqsa.mooo.com
## Launch dev-server with Aqsa on Linux

```sudo -u postgres psql```

```commandline
    CREATE DATABASE aqsa;
    CREATE USER aqsa WITH PASSWORD 'StrongPASSWD';
    ALTER DATABASE aqsa OWNER TO aqsa;
    GRANT ALL PRIVILEGES ON DATABASE "aqsa" TO aqsa;
    \q
```

```commandline
mkdir ~/Python-Django &&
cd ~/Python-Django/ &&
git clone git@github.com:yulaymusin/aqsa.git &&
virtualenv .aqsa-venv &&
source .aqsa-venv/bin/activate &&
pip install -r aqsa/requirements.txt &&
cd ~/Python-Django/aqsa/ &&
touch aqsa_apps/databases.py &&
echo "DATABASES = {" > aqsa_apps/databases.py &&
echo "    'default': {" >> aqsa_apps/databases.py &&
echo "        'ENGINE': 'django.db.backends.postgresql_psycopg2'," >> aqsa_apps/databases.py &&
echo "        'NAME': 'aqsa'," >> aqsa_apps/databases.py &&
echo "        'USER': 'aqsa'," >> aqsa_apps/databases.py &&
echo "        'PASSWORD': 'StrongPASSWD'," >> aqsa_apps/databases.py &&
echo "        'HOST': 'localhost'," >> aqsa_apps/databases.py &&
echo "        'PORT': '5432'," >> aqsa_apps/databases.py &&
echo "    }" >> aqsa_apps/databases.py &&
echo "}" >> aqsa_apps/databases.py &&
python manage.py migrate &&
python manage.py runserver
```
