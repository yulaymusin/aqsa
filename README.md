# Aqsa
Aqsa is Personal Finance Software.

Aqsa is simple, but free software which have some powerful functionality even compare some commercial software.
## Online
https://theaqsa.com
## Launch Aqsa on local
mkdir Workspace && mkdir venv

cd ~/Workspace/

git clone https://github.com/yulaymusin/aqsa.git

cd ~/venv/

virtualenv -p python3.8 aqsa

source aqsa/bin/activate

cd ~/Workspace/aqsa/

pip install -r requirements.txt

touch aqsa_apps/databases.py

nano aqsa_apps/databases.py

!Put your database settings to the file!

python manage.py migrate

python manage.py runserver
