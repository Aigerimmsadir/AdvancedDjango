import os
from django.core.exceptions import ValidationError
from utils.constants import TASK_ALLOWED_EXTS, AVATAR_ALLOWED_EXTS


def task_document_size(value):
    if value.size > 100000000000000000000000:
        raise ValidationError('invalid file size')


def task_document_extension(value):
    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in TASK_ALLOWED_EXTS:
        raise ValidationError(f'not allowed ext, allowed ({TASK_ALLOWED_EXTS})')


def avatar_document_extension(value):
    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in AVATAR_ALLOWED_EXTS:
        raise ValidationError(f'not allowed ext, allowed ({AVATAR_ALLOWED_EXTS})')
