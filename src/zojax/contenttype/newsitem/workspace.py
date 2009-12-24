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
from zope import interface, component
from zope.component import getUtility
from zope.event import notify
from zope import size
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.security.proxy import removeSecurityProxy
from zope.app.container.interfaces import IObjectAddedEvent

from zojax.catalog.interfaces import ICatalog
from zojax.content.type.interfaces import IItem
from zojax.content.type.container import ContentContainer
from zojax.content.space.interfaces import IContentSpace
from zojax.content.space.workspace import WorkspaceFactory

from category import CategoryContainer
from interfaces import _, INewsWorkspace, INewsWorkspaceFactory


class NewsWorkspace(ContentContainer):
    interface.implements(INewsWorkspace)

    title = _(u'News')
    pageSize = 10
    subspaces = False

    @property
    def space(self):
        return self.__parent__

    def news(self, categories=None):
        catalog = getUtility(ICatalog)

        query = dict(
            draftContent = {'any_of': (False,)},
            sort_on='effective', sort_order='reverse',
            typeType = {'any_of': ('News Item',)})

        if categories:
            query['contentTypeNewsCategoryIds'] = {'any_of': set(categories)}

        if self.subspaces:
            query['contentSpaces'] = {'any_of': (self.space.id,)}
        else:
            query['contentSpace'] = {'any_of': (self.space.id,)}

        return catalog.searchResults(**query)


class NewsSized(object):
    component.adapts(INewsWorkspace)
    interface.implements(size.interfaces.ISized)

    def __init__(self, context):
        self.context = context
        self._size = len(self.context.news())

    def sizeForSorting(self):
        return _("news item"), self._size

    def sizeForDisplay(self):
        return size.byteDisplay(self._size)


@component.adapter(INewsWorkspace, IObjectAddedEvent)
def newsWorkspaceAdded(ws, event):
    if 'category' not in ws:
        category = CategoryContainer()
        notify(ObjectCreatedEvent(category))
        ws['category'] = category


class NewsWorkspaceFactory(WorkspaceFactory):
    component.adapts(IContentSpace)
    interface.implements(INewsWorkspaceFactory)

    name = 'news'
    title = _(u'News')
    description = _(u'A news workspace that will show all space news.')
    weight = 2
    factory = NewsWorkspace
