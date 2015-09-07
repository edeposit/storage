#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# Imports =====================================================================
import os
import base64
import tempfile

from kwargs_obj import KwargsObj
from persistent import Persistent
from BalancedDiscStorage import BalancedDiscStorage

from ..settings import PUBLIC_DIR
from ..settings import PRIVATE_DIR
from ..web_tools import compose_full_url

from publication import Publication


# Functions and classes =======================================================

# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!

class DB{{CLASS_NAME}}(Persistent, KwargsObj):
    '''
    Database structure used to store basic metadata about Publications.

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

        bds = BalancedDiscStorage(dirpath)

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
                return bds.add_file(unpacked_file)

    @staticmethod
    def from_comm(pub):
        '''
        Convert communication namedtuple to this class.

        Args:
            pub (obj): :class:`.Publication` instance which will be converted.

        Returns:
            obj: :class:`DBPublication` instance.
        '''
        filename = None
        if pub.b64_data:
            filename = DB{{CLASS_NAME}}._save_to_unique_filename(pub)

        return DB{{CLASS_NAME}}(
% for field in COMMON_FIELDS:
            {{field.name}}=pub.{{field.name}},
% end

            file_pointer=filename
        )

    def to_comm(self, light_request=False):
        '''
        Convert `self` to :class:`.Publication`.

        Returns:
            obj: :class:`.Publication` instance.
        '''
        data = None
        if not light_request:
            with open(self.file_pointer) as unpacked_file:
                with tempfile.TemporaryFile() as b64_file:
                    base64.encode(unpacked_file, b64_file)
                    b64_file.flush()

                    b64_file.seek(0)
                    data = b64_file.read()

        return Publication(
% for field in COMMON_FIELDS:
            {{field.name}}=self.{{field.name}},
% end

            b64_data=data,
            url=compose_full_url(self, uuid_url=True),
            file_pointer=self.file_pointer,
        )

    def __eq__(self, obj):
        if not isinstance(obj, self.__class__):
            return False

        return (
% for field in COMMON_FIELDS[:-1]:
            self.{{field.name}} == obj.{{field.name}} and
% end
            self.{{COMMON_FIELDS[-1].name}} == obj.{{COMMON_FIELDS[-1].name}}
        )

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return hash(
            "".join(x.__repr__() for x in self.__dict__.values())
        )

# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!