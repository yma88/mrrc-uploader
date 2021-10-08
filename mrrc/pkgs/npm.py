"""
Copyright (C) 2021 Red Hat, Inc. (https://github.com/Commonjava/mrrc-uploader)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from mrrc.utils.logs import DEFAULT_LOGGER
import os
import json
import logging


logger = logging.getLogger(DEFAULT_LOGGER)


class NPMPackageMetadata(object):
    """ This NPMPackageMetadata will represent the npm package(not version) package.json which will
        be used in jinja2 or other places.
    """

    def __init__(self, version_metadata):
        self.name = version_metadata.get('name')
        if version_metadata.get('description'):
            self.description = version_metadata.get('description')
        if version_metadata.get('author'):
            self.author = version_metadata.get('author')
        if version_metadata.get('license'):
            self.license = version_metadata.get('license')
        if version_metadata.get('repository'):
            self.repository = version_metadata.get('repository')
        if version_metadata.get('bugs'):
            self.bugs = version_metadata.get('bugs')
        if version_metadata.get('keywords'):
            self.keywords = version_metadata.get('keywords')
        if version_metadata.get('maintainers'):
            self.maintainers = version_metadata.get('maintainers')
        if version_metadata.get('users'):
            self.author = version_metadata.get('users')
        if version_metadata.get('homepage'):
            self.homepage = version_metadata.get('homepage')
        if version_metadata.get('version'):
            self.dist_tags = {'latest': version_metadata.get('version')}
            self.versions = {version_metadata.get('version'): version_metadata}
        if version_metadata.get('time'):
            self.readme = version_metadata.get('time')
        if version_metadata.get('readme'):
            self.readme = version_metadata.get('readme')
        if version_metadata.get('readmeFilename'):
            self.readme = version_metadata.get('readmeFilename')

    def __str__(self) -> str:
        return f'{self.name}\n{self.description}\n{self.author}\n{self.readme}\n{self.homepage}\n' \
               f'{self.license}\n\n'


def scan_for_version(path: str):
    """Scan a file path and find version metadata
    """
    try:
        with open(path, encoding='utf-8') as version_meta_file:
            return json.load(version_meta_file)
    except json.JSONDecodeError:
        logger.error('Error: Failed to validate version metadata!')


def gen_package_meatadata_file(version_metadata, root='/'):
    """Give a version metadata and generate the package metadata based on that.
       The result will write the package metadata file to the appropriate path,
       e.g.: jquery/package.json or @types/jquery/package.json
       Root is like a prefix of the path which defaults to local repo location
    """
    package_metadata = NPMPackageMetadata(version_metadata)

    logger.debug('NPM metadata will generate: %s', package_metadata)
    final_package_metadata_path = os.path.join(root, package_metadata.name, 'package.json')
    try:
        with open(final_package_metadata_path, mode='w', encoding='utf-8') as f:
            json.dump(package_metadata.__dict__, f)
    except FileNotFoundError:
        logger.error(
            'Can not create file %s because of some missing folders', final_package_metadata_path)
