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
"""

$Id$
"""
from pytz import utc
from zc.catalog.catalogindex import SetIndex
from zojax.catalog.utils import Indexable
from zojax.contenttype.newsitem.interfaces import INewsItem


def indexNewsCategoryIds():
    return SetIndex(
        'value', Indexable('zojax.contenttype.newsitem.index.NewsCategoryIds'))


class NewsCategoryIds(object):

    def __init__(self, context, default=None):
        item = INewsItem(context, None)
        if item is None or getattr(item, 'category', None) is None:
            self.value = default
        else:
            self.value = set(item.category)
