import requests, re, os, collections
import logging, traceback, json
import copy
import subprocess
import hashlib
import dateutil.parser
import math

from ConfigParser import ConfigParser
from datetime import datetime
from collections import defaultdict, OrderedDict

from django.conf import settings
from django.forms.models import model_to_dict
from django.db import connection, connections, transaction, IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from raven import Client

from terminal_output import Terminal
from excel_writer import ExcelWriter
from models import ODKForm, RawSubmissions, FormViews, ViewsData, ViewTablesLookup, DictionaryItems, FormMappings, ProcessingErrors, ODKFormGroup
from sql import Query

from .odk_forms import OdkForms

terminal = Terminal()
sentry = Client('http://412f07efec7d461cbcdaf686c3b01e51:c684fccd436e46169c71f8c841ed3b00@sentry.badili.co.ke/3')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
logger = logging.getLogger('ADGG')
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)
request = HttpRequest()


class ADGG():
    def __init__(self):
        return

    def system_stats(self):
        """Get the system summary
        Returns:
            json: A JSON with the system summary
        Raises:
            AssertionError: Incase of empty values, raises an assertion error
        """
        stats = defaultdict(dict)
        stats['farmers'] = defaultdict(dict)
        stats['animals'] = defaultdict(dict)
        stats['formgroups'] = defaultdict(dict)

        with connections['mapped'].cursor() as cursor:
            # get the number of processed farmers
            farmers_q = "SELECT count(*) as count from households"
            cursor.execute(farmers_q)
            farmers = cursor.fetchone()
            if farmers is None:
                raise AssertionError('There was some error while fetching data from the database')

            # get the gender of the household heads
            farmers_gender_q = "SELECT b.t_value, count(*) FROM `hh_attributes` as a inner join dictionary_items as b on a.attribute_type_id=b.id where b.form_group = 'farmer_reg' and parent_node = 'farmergender' group by attribute_type_id"
            cursor.execute(farmers_gender_q)
            farmers_gender = cursor.fetchall()
            if farmers_gender is None:
                raise AssertionError('There was some error while fetching data from the database')

            by_gender = []
            for f_gender in farmers_gender:
                by_gender.append({'name': f_gender[0], 'y': f_gender[1]})

            # get the number of processed animals
            animals_q = "SELECT count(*) as count from animals"
            cursor.execute(animals_q)
            animals = cursor.fetchone()
            if animals is None:
                raise AssertionError('There was some error while fetching data from the database')

            animals_sex_q = "SELECT sex, count(*) from animals group by sex"
            cursor.execute(animals_sex_q)
            animals_sex = cursor.fetchall()
            if animals_sex is None:
                raise AssertionError('There was some error while fetching data from the database')

            by_sex = []
            for a_sex in animals_sex:
                by_sex.append({'name': a_sex[0], 'y': a_sex[1]})

            # get the formgroup processing status
            formgroup_status = self.formgroup_processing_status()

            stats['farmers']['count'] = farmers[0]
            stats['farmers']['by_gender'] = by_gender
            stats['animals']['count'] = animals[0]
            stats['animals']['by_sex'] = by_sex
            stats['formgroups']['processing_status'] = formgroup_status

        return stats

    def formgroup_processing_status(self):
        """Fetch the processing status of the form groups
        Returns:
            JSON: A json with the processing statuses of the form groups
        """
        with connection.cursor() as cursor:
            form_details_q = 'SELECT c.group_name, a.is_processed, count(*) as r_count FROM raw_submissions as a INNER JOIN odkform as b on a.form_id=b.id INNER JOIN form_groups as c on b.form_group_id=c.id GROUP BY c.group_name, a.is_processed ORDER BY c.group_name, b.form_id, a.is_processed'
            cursor.execute(form_details_q)
            odk = OdkForms()
            form_details = odk.dictfetchall(cursor)

            processing_status = defaultdict(dict)
            for res in form_details:
                if res['group_name'] not in processing_status:
                    processing_status[res['group_name']] = []
                    processing_status[res['group_name']].append({
                        'y': res['r_count'],
                        'name': 'Processed' if res['is_processed'] == 1 else 'Unprocesssed'
                    })
                else:
                    processing_status[res['group_name']].append({
                        'y': res['r_count'],
                        'name': 'Processed' if res['is_processed'] == 1 else 'Unprocesssed'
                    })

        return processing_status

    def landing_page_stats(self):
        """Fetches the statistics that will be used in the landing page
        Raises:
            AssertionError: Raises an error if there is nothing in the database
        """
        stats = defaultdict(dict)
        stats['farmers'] = defaultdict(dict)
        stats['animals'] = defaultdict(dict)

        with connections['mapped'].cursor() as cursor:
            # get the number of processed farmers
            farmers_q = "SELECT count(*) as count from households"
            cursor.execute(farmers_q)
            farmers = cursor.fetchone()
            if farmers is None:
                raise AssertionError('There was some error while fetching data from the database')

            # get the number of processed animals
            animals_q = "SELECT count(*) as count from animals"
            cursor.execute(animals_q)
            animals = cursor.fetchone()
            if animals is None:
                raise AssertionError('There was some error while fetching data from the database')

            stats['farmers']['count'] = farmers[0]
            stats['animals']['count'] = animals[0]

        return stats
