from app import app,admin,db
from flask_admin.contrib import sqla
from flask_admin import form

from models import StorageModel

import random
import os


class StorageAdminModel(sqla.ModelView):
    form_extra_fields = {
        'file': form.FileUploadField('file')
    }

    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                hash = random.getrandbits(128)
                ext = storage_file.filename.split('.')[-1]
                path = '%s.%s' % (hash, ext)

                storage_file.save(
                    os.path.join(app.config['STORAGE'], path)
                )

                _form.name.data = _form.name.data or storage_file.filename
                _form.path.data = path
                _form.type.data = ext

                del _form.file

        except Exception as ex:
            pass

        return _form

    def edit_form(self, obj=None):
        return self._change_path_data(
            super(StorageAdminModel, self).edit_form(obj)
        )

    def create_form(self, obj=None):
        return self._change_path_data(
            super(StorageAdminModel, self).create_form(obj)
        )


admin.add_view(StorageAdminModel(StorageModel, db.session))