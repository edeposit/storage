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

from storage.settings import TREE_PROJECT_KEY as PROJECT_KEY

from shared import read_as_base64

from storage.structures.comm.tree import Tree


# Functions and classes =======================================================

# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!

class DBTree(Persistent, KwargsObj):
    '''
    Database structure used to store basic metadata about Trees.

    Attributes:
        name (str): Name of the periodical.
        tree_list (list): List of other trees.
        aleph_id (str): ID used in aleph.
        issn (str): ISSN given to the periodical.
        path (str): ISSN given to the periodical.
    '''
    def __init__(self, **kwargs):
        self.name = None
        self.tree_list = None
        self.aleph_id = None
        self.issn = None
        self.path = None

        self._kwargs_to_attributes(kwargs)

    @classmethod
    def from_comm(cls, pub):
        '''
        Convert communication namedtuple to this class.

        Args:
            pub (obj): :class:`.Tree` instance which will be converted.

        Returns:
            obj: :class:`DBTree` instance.
        '''
        return cls(
            name=pub.name,
            tree_list=pub.tree_list,
            aleph_id=pub.aleph_id,
            issn=pub.issn,
            path=pub.path,

        )

    @property
    def indexes(self):
        """
        Returns:
            list: List of strings, which may be used as indexes in DB.
        """
        return [
            "name",
            "tree_list",
            "aleph_id",
            "issn",
            "path",
        ]

    @property
    def project_key(self):
        return PROJECT_KEY

    def to_comm(self, light_request=False):
        '''
        Convert `self` to :class:`.Tree`.

        Returns:
            obj: :class:`.Tree` instance.
        '''

    def __eq__(self, obj):
        if not isinstance(obj, self.__class__):
            return False

        return (
            self.name == obj.name and
            self.tree_list == obj.tree_list and
            self.aleph_id == obj.aleph_id and
            self.issn == obj.issn and
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