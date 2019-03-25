import requests
import gzip
import shutil
import os
import subprocess

class ThreeDid:

    version_url = 'https://interactome3d.irbbarcelona.org/api/getVersion'
    db_url = 'https://3did.irbbarcelona.org/download/current/3did.sql.gz'

    def __init__(self):
        self.version = None

    # retrieve database version
    def get_version(self):
        self.version = requests.get(ThreeDid.version_url).content

    # download database on disk
    def get_db(self):
        # download archive
        archive_filename = os.path.basename(ThreeDid.db_url)
        archive = requests.get(ThreeDid.db_url)

        # write to disk
        open(archive_filename, 'wb').write(archive.content)

        # extract
        with gzip.open(archive_filename, 'rb') as f_in:
            with open('3did.sql', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    # import database into mysql
    def import_db(self, db):

        # recreate database
        db.execute('drop database if exists 3did')
        db.execute('create database 3did')

        # import downloaded database
        out = subprocess.check_output(['mysql', '-u', 'root', '--show-warnings', '-e', 'use 3did; source 3did.sql;'])
        print(out.decode())

    def test_db(self, db):
        db.execute('use 3did')
        db.execute('show tables')
        for row in db.fetchall():
            print(row)
