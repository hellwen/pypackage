##PyPackage

##Install

###pyenv

        pyenv virtualenv pypackage

###Prerequisite

        sudo pacman -S libxml2 libxslt
        pip install -r requirements.txt

###Custom the Configuration
        
        pypackage/config.cfg

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


