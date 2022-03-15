"""
Разные мелкие утилитки, которыми можно воспользоваться из любого места
"""
import os.path, stat

from django.core.exceptions import ValidationError
from fcmadmin.settings import IMAGE_SIZE, MEDIA_ROOT, MEDIA_URL
from phonenumbers import parse, is_valid_number, format_number, PhoneNumberFormat, NumberParseException
from django.utils.translation import gettext_lazy as _
from django.db import connection
import shutil


def get_image_upload(instance, file):
    """
    Строим путь к изображениям. Формат: media/app_name/class_name/photo/id/file
    """
    module_name = instance.__module__.split('.')[0]
    class_name = instance.__class__.__name__.lower()
    if instance.id:
        some_id = instance.id
    else:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM public.\"{module_name}_{class_name}_id_seq\";")
            some_id = cursor.fetchone()
        some_id = some_id[0]
        if some_id != 0 or some_id is not None:
            some_id += 1
        else:
            some_id = 0
    if class_name.find('photo') != -1:
        path_to_file = os.path.join(MEDIA_ROOT, module_name, class_name,
                                    'photo', some_id, file)
    elif class_name.find('logo') != -1:
        path_to_file = os.path.join(MEDIA_ROOT, module_name, class_name,
                                    'logo', some_id, file)
    else:
        raise Exception('Поле для фото/логотипа не найдено')
    return path_to_file


def get_file_upload(instance, file=None):
    """
    Строим путь к файлам. Формат: media/app_name/class_name/files/id/file
    """
    module_name = instance.__module__.split('.')[0]
    class_name = instance.__class__.__name__.lower()
    if instance.id:
        some_id = instance.id
    else:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM public.\"{module_name}_{class_name}_id_seq\";")
            some_id = cursor.fetchone()
        some_id = some_id[0]
        if some_id != 0 or some_id is not None:
            some_id += 1
        else:
            some_id = 0
    # если хотим получить весь путь к файлу - пользователь загружает извне
    if file is not None:
        return f'{module_name}/{class_name}/files/{some_id}/{file}'
    # если нет - строим путь к файлу, который создаем самостоятельно - создадим путь в
    # файловой системе и вернем его.
    else:
        path = os.path.join(module_name, class_name, 'files', str(some_id))
        return path


def get_video_upload(instance, file):
    """
    Строим путь к файлам. Формат: media/app_name/class_name/files/id/file
    """
    module_name = instance.__module__.split('.')[0]
    class_name = instance.__class__.__name__.lower()
    if instance.id:
        some_id = instance.id
    else:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM public.\"{module_name}_{class_name}_id_seq\";")
            some_id = cursor.fetchone()
        some_id = some_id[0]
        if some_id != 0 or some_id is not None:
            some_id += 1
        else:
            some_id = 0
    path_to_file = os.path.join(MEDIA_ROOT, module_name, class_name,
                                'videos', some_id, file)
    return path_to_file


def validate_photo_size(file):
    """
    Проверка размера изображения. Размер не должен быть больше, чем limit.
    """
    if file.size > IMAGE_SIZE * 1024 * 1024:
        raise ValidationError(f'_("Max file size - {IMAGE_SIZE} Mb")')


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal"""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def delete_old_file(path_file):
    """
    Удаление старого файла из файловой системы.
    """
    if os.path.exists(path_file):
        splitted_path = path_file.split('/')
        # Если это изображение, которое находится в папке одно(больше не предусмотрено моделью), удалим с папкой
        if path_file.find('logo') != -1 or path_file.find('photo') != -1:
            path_file = '/'.join(s for s in splitted_path[0:len(splitted_path)-1])
            shutil.rmtree(path_file, onerror=remove_readonly)
        else:
            os.remove(path_file)
