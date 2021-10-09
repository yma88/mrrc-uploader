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
        self.name = version_metadata.get('name', None)
        self.description = version_metadata.get('description', None)
        self.author = version_metadata.get('author', None)
        self.license = version_metadata.get('license', None)
        self.repository = version_metadata.get('repository', None)
        self.bugs = version_metadata.get('bugs', None)
        self.keywords = version_metadata.get('keywords', None)
        self.maintainers = version_metadata.get('maintainers', None)
        self.author = version_metadata.get('users', None)
        self.homepage = version_metadata.get('homepage', None)
        self.dist_tags = {'latest': version_metadata.get('version')}
        self.versions = {version_metadata.get('version'): version_metadata}
        self.readme = version_metadata.get('time', None)
        self.readme = version_metadata.get('readme', None)
        self.readme = version_metadata.get('readmeFilename', None)

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
            json.dump(__del_none(package_metadata.__dict__.copy()), f)
    except FileNotFoundError:
        logger.error(
            'Can not create file %s because of some missing folders', final_package_metadata_path)


def __del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            __del_none(value)
    return d
