"""
Addressable Paragraphs
------------------------
In converting from MD to html images are wrapped in <p> objects.
This plugin gives those paragraphs the 'img' class for styling enhancements.
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
                    caption = soup.new_tag('span',**{'class':'caption'})
                    for i in reversed(p.contents):
                        if i.name != 'img': #if it is not an <img> tag
                            caption.insert(0,i.extract())
                    p.append(caption)

        instance._content = soup.decode()


def register():
    signals.content_object_init.connect(content_object_init)
