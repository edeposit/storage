#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# Imports =====================================================================
import os
import base64
import zipfile
import os.path
import tempfile

from kwargs_obj import KwargsObj
from persistent import Persistent
% if CLASS_NAME == "Publication":
from BalancedDiscStorage import BalancedDiscStorage
% elif CLASS_NAME == "Archive":
from BalancedDiscStorage import BalancedDiscStorageZ
% end

% if CLASS_NAME == "Publication":
from ..settings import PUB_PROJECT_KEY as PROJECT_KEY
from ..settings import PUBLIC_DIR
from ..settings import PRIVATE_DIR
% elif CLASS_NAME == "Archive":
from ..settings import ARCH_PROJECT_KEY as PROJECT_KEY
from ..settings import ARCHIVE_DIR as PUBLIC_DIR
from ..settings import ARCHIVE_DIR as PRIVATE_DIR
% end

from ..web_tools import compose_full_url

from shared import path_to_zip
from shared import read_as_base64

from {{CLASS_NAME.lower()}} import {{CLASS_NAME}}


# Functions and classes =======================================================

# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!

class DB{{CLASS_NAME}}(Persistent, KwargsObj):
    '''
    Database structure used to store basic metadata about {{CLASS_NAME}}s.

    Attributes:
% for field in DATABASE_FIELDS:
        {{field.name}} {{field.docstring}}
% end
    '''
    def __init__(self, **kwargs):
% for field in DATABASE_FIELDS:
        self.{{field.name}} = None
% end

        self._kwargs_to_attributes(kwargs)

    @staticmethod
    def _save_to_unique_filename(pub):
        dirpath = PUBLIC_DIR if pub.is_public else PRIVATE_DIR

        if not os.path.exists(dirpath):
            raise IOError("`%s` doesn't exists!" % dirpath)

% if CLASS_NAME == "Publication":
        bds = BalancedDiscStorage(dirpath)
% elif CLASS_NAME == "Archive":
        bdsz = BalancedDiscStorageZ(dirpath)
% end

        # this is optimization for big files, which take big chunks of memory,
        # if copied multiple times as string
        with tempfile.TemporaryFile() as b64_file:
            b64_file.write(pub.b64_data)
            b64_file.flush()

            # unpack base64 data
            b64_file.seek(0)
            with tempfile.TemporaryFile() as unpacked_file:
                base64.decode(b64_file, unpacked_file)
                unpacked_file.flush()

                unpacked_file.seek(0)
% if CLASS_NAME == "Publication":
                return bds.add_file(unpacked_file)
% elif CLASS_NAME == "Archive":
                return bdsz.add_archive_as_dir(unpacked_file)
% end

    @staticmethod
    def from_comm(pub):
        '''
        Convert communication namedtuple to this class.

        Args:
            pub (obj): :class:`.{{CLASS_NAME}}` instance which will be converted.

        Returns:
            obj: :class:`DB{{CLASS_NAME}}` instance.
        '''
        filename = None
        if pub.b64_data:
            filename = DB{{CLASS_NAME}}._save_to_unique_filename(pub)

        return DB{{CLASS_NAME}}(
% for field in SAVEABLE_FIELDS:
            {{field.name}}=pub.{{field.name}},
% end

            file_pointer=filename
        )

    @property
    def indexes(self):
        """
        Returns:
            list: List of strings, which may be used as indexes in DB.
        """
        return [
% for field in DATABASE_FIELDS:
            "{{field.name}}",
% end
        ]

    @property
    def project_key(self):
        return PROJECT_KEY

    def to_comm(self, light_request=False):
        '''
        Convert `self` to :class:`.{{CLASS_NAME}}`.

        Returns:
            obj: :class:`.{{CLASS_NAME}}` instance.
        '''
% if CLASS_NAME == "Publication":  # ==========================================
        data = None
        if not light_request:
            data = read_as_base64(self.file_pointer)

        return {{CLASS_NAME}}(
    % for field in SAVEABLE_FIELDS:
            {{field.name}}=self.{{field.name}},
    % end

            b64_data=data,
            url=compose_full_url(self, uuid_url=True),
            file_pointer=self.file_pointer,
        )
% elif CLASS_NAME == "Archive":  # ============================================
        data = None
        if not light_request:
            tmp_fn = path_to_zip(self.dir_pointer)
            data = read_as_base64(tmp_fn)
            os.unlink(tmp_fn)

        return {{CLASS_NAME}}(
    % for field in SAVEABLE_FIELDS:
            {{field.name}}=self.{{field.name}},
    % end

            b64_data=data,
            dir_pointer=self.dir_pointer,
        )
% end  # ======================================================================

    def __eq__(self, obj):
        if not isinstance(obj, self.__class__):
            return False

        return (
% for field in SAVEABLE_FIELDS[:-1]:
            self.{{field.name}} == obj.{{field.name}} and
% end
            self.{{SAVEABLE_FIELDS[-1].name}} == obj.{{SAVEABLE_FIELDS[-1].name}}
        )

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return hash(
            "".join(x.__repr__() for x in self.__dict__.values())
        )

# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
