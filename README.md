##PyPackage

##Install

###Pythonbre

        sudo esay_install pip
        sudo esay_install pythonbrew

###Create env

        pythonbrew venv create pypackage

###Prerequisite

        pip install -r requirements.txt

###Custom the Configuration
        
        pypress/config.cfg

###Sync database

        python manage.py createall

###Run

        python manage.py runserver

##Example

###Create User

Admin:

        python manage.py createadmin

###Generate Admin active code

        python manage.py createcode -r admin


