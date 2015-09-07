#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Classes =====================================================================
class Field(object):
    def __init__(self, name, docstring, is_comm_field, is_db_field):
        self.name = name
        self.docstring = docstring
        self.is_comm_field = is_comm_field
        self.is_db_field = is_db_field

    def __repr__(self):
        return "Field(name)" % self.name


# Variables ===================================================================
CLASS_NAME = "Publication"


FIELDS = [
    Field(
        name="title",
        docstring="(str): Title of the publication.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="author",
        docstring="(str): Name of the author.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="pub_year",
        docstring="(str): Year when the publication was released.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="isbn",
        docstring="(str): ISBN for the publication.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="urnnbn",
        docstring="(str): URN:NBN for the publication.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="uuid",
        docstring="(str): UUID string to pair the publication with edeposit.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="aleph_id",
        docstring="(str): ID used in aleph.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="producent_id",
        docstring="(str): ID used for producent.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="is_public",
        docstring="(bool): Is the file public?",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="filename",
        docstring="(str): Original filename.",
        is_comm_field=True,
        is_db_field=True,
    ),

    # comm fields
    Field(
        name="b64_data",
        docstring="(str): Base64 encoded data ebook file.",
        is_comm_field=True,
        is_db_field=False,
    ),
    Field(
        name="url",
        docstring="(str): URL in case that publication is public.",
        is_comm_field=True,
        is_db_field=False,
    ),
    Field(
        name="file_pointer",
        docstring="(str): Pointer to the file on the file server.",
        is_comm_field=True,
        is_db_field=False,
    ),

    # DB fields
    Field(
        name="file_pointer",
        docstring="(str): Pointer to the file on the file server.",
        is_comm_field=False,
        is_db_field=True,
    ),
]

COMMON_FIELDS = [
    field
    for field in FIELDS
    if field.is_comm_field and field.is_db_field
]

COMMUNICATION_FIELDS = [
    field
    for field in FIELDS
    if field.is_comm_field
]

DATABASE_FIELDS = [
    field
    for field in FIELDS
    if field.is_db_field
]

ONLY_DB_FIELDS = [
    field
    for field in FIELDS
    if field.is_db_field and not field.is_comm_field
]