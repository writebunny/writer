#!/bin/bash
python manage.py collectstatic --noinput --settings="main.settings_live"
appcfg.py update ./
