#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# Imports =====================================================================
import os
import uuid
import base64

from kwargs_obj import KwargsObj
from persistent import Persistent

from ..settings import PUBLIC_DIR
from ..settings import PRIVATE_DIR

from publication import Publication


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
        self.file_pointer = None

        self._kwargs_to_attributes(kwargs)

    @staticmethod
    def _save_to_unique_filename(pub):
        dirpath = PUBLIC_DIR if pub.is_public else PRIVATE_DIR

        if not os.path.exists(dirpath):
            raise IOError("\%s doesn't exists!" % dirpath)

        # get uniq filename
        filename = "/"
        while os.path.exists(filename):
            filename = os.path.join(dirpath, str(uuid.uuid4()))

        with open(filename, "wb") as f:
            f.write(
                base64.b64decode(pub.b64_data)
            )

        return filename

    @staticmethod
    def from_comm(pub):
        filename = None
        if pub.b64_data:
            filename = DBPublication._save_to_unique_filename(pub)

        return DBPublication(
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

            file_pointer=filename
        )

    def to_comm(self):
        with open(self.file_pointer) as f:
            data = base64.b64encode(f.read())

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

            b64_data=data
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
            self.filename == obj.filename
        )

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return hash(
            "".join(x.__repr__() for x in self.__dict__.values())
        )

# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
