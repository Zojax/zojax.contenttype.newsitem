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
from zope import component
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zojax.cache.tag import ContextTag
from zojax.content.type.interfaces import IDraftedContent

from interfaces import INewsItemType

NewsItemsTag = ContextTag('zojax.contenttype.newsitems')


@component.adapter(INewsItemType, IObjectModifiedEvent)
def newsItemHandler(ob, ev):
    if not IDraftedContent.providedBy(ob):
        try:
            NewsItemsTag.update(ob)
        except TypeError:
            pass
