#!/usr/bin/env python

# -*- coding: utf-8 -*- #

# Page Meta-Data
# ------------------------
# Insert meta-data about the generated file into the resulting HMTL.
# Copyright (C) 2019  Roel Roscam Abbing
#
# Support your local Low-Tech Magazine:
# https://solar.lowtechmagazine.com/donate.html

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from pelican import signals
from bs4 import BeautifulSoup
import os


def get_printable_size(byte_size):
    """
    Thanks Pobux!
    https://gist.github.com/Pobux/0c474672b3acd4473d459d3219675ad8
    """
    BASE_SIZE = 1024.00
    MEASURE = ["B", "KB", "MB", "GB", "TB", "PB"]

    def _fix_size(size, size_index):
        if not size:
            return "0"
        elif size_index == 0:
            return str(size)
        else:
            return "{:.2f}".format(size)

    current_size = byte_size
    size_index = 0

    while current_size >= BASE_SIZE and len(MEASURE) != size_index:
        current_size = current_size / BASE_SIZE
        size_index = size_index + 1

    size = _fix_size(current_size, size_index)
    measure = MEASURE[size_index]
    return size + measure

def get_assets(soup):
    assets = []
    for a in soup.findAll('link', {'rel':['apple-touch-icon','icon','stylesheet']}):
        a = a['href'].split('?')[0]
        if a not in assets:
            assets.append(a)
    return assets

def get_media(html_file):
    """
    Currently only images because I, for one, am lazy.
    """
    html_file = open(html_file).read()
    soup = BeautifulSoup(html_file, 'html.parser')
    media = []

    for img in soup(['img', 'object']):
        media.append(img['src'])

    featured_images = soup.findAll('div', {'class':'featured-img'})
    for fi in featured_images:
        fi = fi['style']
        start = fi.find("url('")
        end = fi.find("');")
        url = fi[start+len("url('"):end]
        media.append(url)

    assets = get_assets(soup)
    media = list(set(media+assets))  # duplicate media don't increase page size
    return media, soup

def generate_metadata(path, context):
    output_path = context['OUTPUT_PATH']
    output_file = context['output_file']
    siteurl = context['SITEURL']
    plugins = context['PLUGINS']
    subsites = False

    if 'i18n_subsites' in plugins:
        subsites = True
        lang = context['DEFAULT_LANG']
        general_output_path = output_path.replace(lang, '')
        siteurl = context['main_siteurl']

    media_size = 0
    # enumerate all media displayed on the page
    media, soup = get_media(path) #reuse the same soup to limit calculation

    for m in media:
        # filter out SITEURL to prevent trouble
        # join output path to file, need to strip any leading slash for os.path
        if subsites:
            file_name = m.replace(context['main_siteurl']+'/', '')
            m = os.path.join(general_output_path, file_name.strip('/'))
        else:
            file_name = m.replace(context['SITEURL']+'/', '')
            m = os.path.join(output_path, file_name.strip('/'))
        #print(m)
        if os.path.exists(m):
            #print(m, 'exists')
            media_size = media_size + os.path.getsize(m)

    current_file = os.path.join(output_path, output_file)
    file_size = os.path.getsize(current_file)

    file_size = file_size + media_size
    metadata = get_printable_size(file_size)
    metadata = get_printable_size(file_size+len(metadata))  # cursed code is cursed

    insert_metadata(path, metadata, soup)

def insert_metadata(output_file, metadata, soup):
        tag = soup.find('div', {'id':'page-size'})
        if tag:
            with open(output_file,'w') as f:
                tag.string = '{}'.format(metadata)
                f.write(str(soup))

def register():
    signals.content_written.connect(generate_metadata)
