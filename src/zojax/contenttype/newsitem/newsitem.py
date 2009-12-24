##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" news item implementation

$Id$
"""
import rwproperty
from zope import interface, component
from zope.size import byteDisplay
from zope.size.interfaces import ISized
from zope.schema.fieldproperty import FieldProperty
from zope.dublincore.interfaces import IDCPublishing

from zojax.richtext.field import RichTextProperty
from zojax.content.type.item import PersistentItem
from zojax.content.type.contenttype import ContentType
from zojax.content.type.searchable import ContentSearchableText

from interfaces import INewsItem, INewsWorkspace


class NewsItem(PersistentItem):
    interface.implements(INewsItem)

    text = RichTextProperty(INewsItem['text'])
    category = FieldProperty(INewsItem['category'])

    @rwproperty.getproperty
    def date(self):
        date = self.__dict__.get('date', None)

        if date is not None and IDCPublishing(self).effective is None:
            IDCPublishing(self).effective = date

        return date

    @rwproperty.setproperty
    def date(self, value):
        self.__dict__['date'] = value
        IDCPublishing(self).effective = value


class Sized(object):
    component.adapts(INewsItem)
    interface.implements(ISized)

    def __init__(self, context):
        self.context = context

        self.size = len(context.title) + \
                    len(context.description) + \
                    len(context.text)

    def sizeForSorting(self):
        return "byte", self.size

    def sizeForDisplay(self):
        return byteDisplay(self.size)


class SearchableText(ContentSearchableText):
    component.adapts(INewsItem)

    def getSearchableText(self):
        text = super(SearchableText, self).getSearchableText()

        try:
            return text + u' ' + self.content.text.text
        except AttributeError:
            return text
