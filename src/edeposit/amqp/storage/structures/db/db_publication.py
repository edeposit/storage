#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# Imports =====================================================================
import os
import base64
import os.path
import tempfile

from kwargs_obj import KwargsObj
from persistent import Persistent
from BalancedDiscStorage import BalancedDiscStorage

from storage.settings import PUBLIC_DIR
from storage.settings import PRIVATE_DIR
from storage.settings import PUB_PROJECT_KEY as PROJECT_KEY

from storage.web_tools import compose_full_url

from shared import read_as_base64

from storage.structures.comm.publication import Publication


# Functions and classes =======================================================

# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!

class DBPublication(Persistent, KwargsObj):
    '''
    Database structure used to store basic metadata about Publications.

    Attributes:
        title (str): Title of the publication.
        author (str): Name of the author.
        pub_year (str): Year when the publication was released.
        isbn (str): ISBN for the publication.
        urnnbn (str): URN:NBN for the publication.
        uuid (str): UUID string to pair the publication with edeposit.
        aleph_id (str): ID used in aleph.
        producent_id (str): ID used for producent.
        is_public (bool): Is the file public?
        filename (str): Original filename.
        is_periodical (bool): Is the publication periodical?
        path (str): Path in the tree (used for periodicals).
        file_pointer (str): Pointer to the file on the file server.
    '''
    def __init__(self, **kwargs):
        self.title = None
        self.author = None
        self.pub_year = None
        self.isbn = None
        self.urnnbn = None
        self.uuid = None
        self.aleph_id = None
        self.producent_id = None
        self.is_public = None
        self.filename = None
        self.is_periodical = None
        self.path = None
        self.file_pointer = None

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

    @classmethod
    def from_comm(cls, pub):
        '''
        Convert communication namedtuple to this class.

        Args:
            pub (obj): :class:`.Publication` instance which will be converted.

        Returns:
            obj: :class:`DBPublication` instance.
        '''
        filename = None
        if pub.b64_data:
            filename = cls._save_to_unique_filename(pub)

        return cls(
            title=pub.title,
            author=pub.author,
            pub_year=pub.pub_year,
            isbn=pub.isbn,
            urnnbn=pub.urnnbn,
            uuid=pub.uuid,
            aleph_id=pub.aleph_id,
            producent_id=pub.producent_id,
            is_public=pub.is_public,
            filename=pub.filename,
            is_periodical=pub.is_periodical,
            path=pub.path,

            file_pointer=filename
        )

    @property
    def indexes(self):
        """
        Returns:
            list: List of strings, which may be used as indexes in DB.
        """
        return [
            "title",
            "author",
            "pub_year",
            "isbn",
            "urnnbn",
            "uuid",
            "aleph_id",
            "producent_id",
            "is_public",
            "filename",
            "is_periodical",
            "path",
            "file_pointer",
        ]

    @property
    def project_key(self):
        return PROJECT_KEY

    def to_comm(self, light_request=False):
        '''
        Convert `self` to :class:`.Publication`.

        Returns:
            obj: :class:`.Publication` instance.
        '''
        data = None
        if not light_request:
            data = read_as_base64(self.file_pointer)

        url = compose_full_url(self, uuid_url=True)

        return Publication(
            title=self.title,
            author=self.author,
            pub_year=self.pub_year,
            isbn=self.isbn,
            urnnbn=self.urnnbn,
            uuid=self.uuid,
            aleph_id=self.aleph_id,
            producent_id=self.producent_id,
            is_public=self.is_public,
            filename=self.filename,
            is_periodical=self.is_periodical,
            path=self.path,

            b64_data=data,
            url=url,
            file_pointer=self.file_pointer,
        )

    def __eq__(self, obj):
        if not isinstance(obj, self.__class__):
            return False

        return (
            self.title == obj.title and
            self.author == obj.author and
            self.pub_year == obj.pub_year and
            self.isbn == obj.isbn and
            self.urnnbn == obj.urnnbn and
            self.uuid == obj.uuid and
            self.aleph_id == obj.aleph_id and
            self.producent_id == obj.producent_id and
            self.is_public == obj.is_public and
            self.filename == obj.filename and
            self.is_periodical == obj.is_periodical and
            self.path == obj.path
        )

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return hash(
            "".join(x.__repr__() for x in self.__dict__.values())
        )

# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
