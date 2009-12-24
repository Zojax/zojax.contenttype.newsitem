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
"""News items portlet

$Id$
"""
from operator import attrgetter
from zope import interface
from zope.component import getUtility
from zope.traversing.api import getPath
from zope.app.component.hooks import getSite

from zojax.cache.view import cache
from zojax.layout.interfaces import ILayout
from zojax.catalog.interfaces import ICatalog
from zojax.content.space.interfaces import ISpace
from zojax.portlet.cache import PortletId, PortletModificationTag

from zojax.contenttype.newsitem.cache import NewsItemsTag
from zojax.contenttype.newsitem.portlets.interfaces import INewsItemsPortlet


class NewsItemsPortlet(object):
    interface.implements(INewsItemsPortlet)

    news = ()
    categories = None

    def __init__(self, context, request, manager, view):
        super(NewsItemsPortlet, self).__init__(context, request, manager, view)

        if self.source == 3:
            context = getSite()
        else:
            if ILayout.providedBy(view):
                context = view.maincontext

            while not ISpace.providedBy(context):
                context = getattr(context, '__parent__', None)
                if context is None:
                    break

            if context is None:
                context = getSite()

            if self.source == 1:
                context = context.get('news', context)
        self.context = context

    def update(self):
        super(NewsItemsPortlet, self).update()

        query = dict(
            sort_on='effective', sort_order='reverse',
            isDraft = {'any_of': (False,)},
            typeType = {'any_of': ('News Item',)})

        if self.source == 3:
            query['searchContext'] = self.context,
        else:
            query['traversablePath'] = {'any_of': (self.context,)}

        if self.categories:
            query['contentTypeNewsCategoryIds'] = {'any_of': self.categories}

        results = getUtility(ICatalog).searchResults(**query)
        if results:
            self.news = results[:self.number]
            self.intids = results.uidutil

    def getCategories(self, item):
        queryObject = self.intids.queryObject
        categories = []
        for uid in item.category:
            category = queryObject(uid)
            if category is not None:
                categories.append(category)
        categories.sort(key=attrgetter('title'))
        return categories

    def isAvailable(self):
        if not self.news:
            return False

        return super(NewsItemsPortlet, self).isAvailable()

    @cache(PortletId(), PortletModificationTag, NewsItemsTag)
    def updateAndRender(self):
        return super(NewsItemsPortlet, self).updateAndRender()
