#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from string import Template


# Variables ===================================================================
CLASS_NAME = "Publication"

COMMON_FIELDS = [
    ["title", "(str): Title of the publication."],
    ["author", "(str): Name of the author."],
    ["pub_year", "(str): Year when the publication was released."],
    ["isbn", "(str): ISBN for the publication."],
    ["urnnbn", "(str): URN:NBN for the publication."],
    ["uuid", "(str): UUID string to pair the publication with edeposit."],
    ["is_public", "(bool): Is the file public?"],
    ["filename", "(str): Original filename."]
]

COMMUNICATION_FIELDS = [
    ["b64_data", "(str): Base64 encoded data ebook file."],
]

DATABASE_FIELDS = [
    ["file_pointer", "(str): Pointer to the file on the file server."],
]

TEMPLATE = """#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# Imports =====================================================================
$imports


# Functions and classes =======================================================

# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
$classes
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
"""

COMMUNICATION_STRUCTURE = """
fields = [
    $fields
]


class $class_name(namedtuple('$class_name', fields)):
    '''
    Communication structure used to sent data to `storage` subsystem over AMQP.

    Attributes:
        $docstring_fields
    '''
"""

DATABASE_IMPORTS = """
import os
import uuid
import base64

from kwargs_obj import KwargsObj
from persistent import Persistent

from ..settings import PUBLIC_DIR
from ..settings import PRIVATE_DIR

from publication import Publication

""".strip()


DATABASE_STRUCTURE = """
class DB$class_name(Persistent, KwargsObj):
    '''
    Database structure used to store basic metadata about Publications.

    Attributes:
        $docstring_fields
    '''
    def __init__(self, **kwargs):
        $fields
        self._kwargs_to_attributes(kwargs)

    @staticmethod
    def from_comm(pub):
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

        return DB$class_name(
            $comm_to_db_fields
            file_pointer=filename
        )

    def to_comm(self):
        with open(self.file_pointer) as f:
            data = base64.b64encode(f.read())

        return $class_name(
            $db_to_comm_fields
            b64_data=data
        )
"""


# Functions & classes =========================================================
def _get_docstring_fields(fields):
    return "\n        ".join(
        name + " " + description
        for name, description in fields
    )


def generate_communication():
    fields = "\n    ".join(
        '"%s",' % name
        for name, x in COMMON_FIELDS + COMMUNICATION_FIELDS
    )

    return Template(COMMUNICATION_STRUCTURE).substitute(
        fields=fields,
        class_name=CLASS_NAME,
        docstring_fields=_get_docstring_fields(
            COMMON_FIELDS + COMMUNICATION_FIELDS
        )
    )


def generate_database():
    fields = "        ".join(
        "self.%s = None\n" % name
        for name, x in COMMON_FIELDS + DATABASE_FIELDS
    )

    comm_to_db_fields = "            ".join(
        "%s=pub.%s,\n" % (name, name)
        for name, x in COMMON_FIELDS
    )

    db_to_comm_fields = "            ".join(
        "%s=self.%s,\n" % (name, name)
        for name, x in COMMON_FIELDS
    )

    return Template(DATABASE_STRUCTURE).substitute(
        fields=fields,
        class_name=CLASS_NAME,
        comm_to_db_fields=comm_to_db_fields,
        db_to_comm_fields=db_to_comm_fields,
        docstring_fields=_get_docstring_fields(
            COMMON_FIELDS + DATABASE_FIELDS
        )
    )


def generate_structures():
    with open("publication.py", "w") as f:
        f.write(
            Template(TEMPLATE).substitute(
                imports="from collections import namedtuple",
                classes=generate_communication()
            )
        )

    with open("db_publication.py", "w") as f:
        f.write(
            Template(TEMPLATE).substitute(
                imports=DATABASE_IMPORTS,
                classes=generate_database()
            )
        )


# Main program ================================================================
if __name__ == '__main__':
    generate_structures()
