import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commendaIo.settings")

import django
django.setup()

from django.core.management import call_command

from home import views
import json

views.addRow(json.dumps({"method": "POST",
              "POST":{
                  'start_date': '01/01/2025',
                  'end_date': '01/01/2030',
                  'value' : 'newValueTest'
              }}), 1)