import os
import sys
import subprocess
import platform
from fCoffeeProject.settings import DEBUG, MEDIA_URL, TEMP_FILES
import cloudinary
from django.http.response import HttpResponse
import tempfile

from django.core.files.base import File


import pdfkit
from django.template import loader
from base.services import get_file_upload

upload_preset = 'nftqyh84'

options = {
    # 'font': 'SF UI Text',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    # 'header-html': 'http://127.0.0.1:8000/docs/header/',
    'header-html': 'vast-mesa-53559.herokuapp.com/docs/header/',
    'custom-header': 'template.html',
    'quiet': None,
    'enable-local-file-access': True,
}

# if DEBUG:
#     options['header-html'] = 'http://127.0.0.1:8000/docs/header/'
# else:
#     options['header-html'] = 'vast-mesa-53559.herokuapp.com/docs/header/'


def _get_pdfkit_config():
    if platform.system() == "Windows":
        pdfkit_config = pdfkit.configuration(
            wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
    else:
        os.environ['PATH'] += os.pathsep + os.path.dirname(sys.executable)
        WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')],
                                           stdout=subprocess.PIPE).communicate()[0].strip()
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
    return pdfkit_config


def generate_file(instance):
    context = {
        'text_string': instance.text,
    }
    template_object = loader.get_template(template_name='pdfGenerator/UserLicenses/base_template.html')
    rendered_template = template_object.render(context)
    if not os.path.exists(TEMP_FILES):
        os.mkdir(TEMP_FILES)
    file_path = os.path.join(TEMP_FILES, 'agreements.pdf')

    pdfkit.from_string(rendered_template, file_path, options, configuration=_get_pdfkit_config())
        # upload_file(path_to_file_with_media,
        #             folder=paths_to_file[1],
        #             public_id='file.pdf',
        #             unique_filename=False,
        #             resource_type='raw',
        #             access_control={
        #                 'access_type': "anonymous",
        #             }
        #             )
    return file_path


# def upload_file(file, **upload_options):
#     cloudinary.uploader.unsigned_upload(
#         open(file, "rb"), upload_preset, **upload_options
#     )
