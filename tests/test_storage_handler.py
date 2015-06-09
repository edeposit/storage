#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import shutil
import os.path
import tempfile
import subprocess
from string import Template
from multiprocessing import Process

import pytest

import storage
from storage import zconf
from storage import settings
from storage import storage_handler
from storage.structures import DBPublication


# Variables ===================================================================
TMP_DIR = None
SERV = None


# Fixtures ====================================================================
def data_context(fn):
    path = os.path.join(os.path.dirname(__file__), "data")

    with open(os.path.join(path, fn)) as f:
        return f.read()


@pytest.fixture
def full_publication():
    return DBPublication(
        title="title",
        author="author",
        pub_year="2015",
        isbn="ISBN",
        urnnbn="URN",
        uuid="UUID",
        is_public=True,
        filename="/home/xex.pdf",
        file_pointer="/tmp/uuid287378",
    )


# Tests =======================================================================
def setup_module(module):
    global TMP_DIR
    TMP_DIR = tempfile.mkdtemp()

    # monkey patch the paths
    settings.ZCONF_PATH = TMP_DIR
    zconf.ZCONF_PATH = TMP_DIR

    # write ZEO server config to  temp directory
    zeo_conf_path = os.path.join(TMP_DIR, "zeo.conf")
    with open(zeo_conf_path, "w") as f:
        f.write(
            Template(data_context("zeo.conf")).substitute(path=TMP_DIR)
        )

    # write client config to temp directory
    client_config_path = os.path.join(TMP_DIR, "zeo_client.conf")
    with open(client_config_path, "w") as f:
        f.write(data_context("zeo_client.conf"))

    # run the ZEO server
    def run_zeo():
        # subprocess.check_call("runzeo -C " + zeo_conf_path, shell=True)
        import sh  # TODO: remove
        sh.runzeo(C=zeo_conf_path)

    global SERV
    SERV = Process(target=run_zeo)
    SERV.start()


def test_get_db_connectors():
    connectors = storage_handler._get_db_connectors()

    assert len(list(connectors)) > 1


def test_check_pub_type():
    with pytest.raises(storage_handler.InvalidType):
        storage_handler._check_pub_type(object)

    with pytest.raises(storage_handler.InvalidType):
        storage_handler._check_pub_type(
            storage.structures.publication.Publication(*range(9))
        )

    storage_handler._check_pub_type(DBPublication())


def test_save_publication(full_publication):
    storage_handler.save_publication(full_publication)


def teardown_module(module):
    SERV.terminate()
    shutil.rmtree(TMP_DIR)
