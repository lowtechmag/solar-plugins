"""
Addressable Paragraphs
------------------------
In converting from .md to .html, images are wrapped in <p> tags.
This plugin gives those paragraphs the 'img' class for styling enhancements.
In case there is any description immediately following that image, it is wrapped in another paragraph with the 'caption' class.

Copyright (C) 2018  Roel Roscam Abbing

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
from pelican import signals
from bs4 import BeautifulSoup

def content_object_init(instance):

    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content, 'html.parser')

        for p in soup(['p', 'object']):
                if p.findChild('img'):
                    p.attrs['class'] = 'img'
                    caption = soup.new_tag('p',**{'class':'caption'})
                    if len(p.contents) > 1: #if we have more than just the <img> tag
                        for i in reversed(p.contents):
                            if i.name != 'img': #if it is not an <img> tag
                                caption.insert(0,i.extract())
                        p.insert_after(caption)

        instance._content = soup.decode()


def register():
    signals.content_object_init.connect(content_object_init)
