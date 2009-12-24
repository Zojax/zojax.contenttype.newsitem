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
from operator import attrgetter
from zope.component import getUtility
from zope.traversing.api import getPath
from zope.app.intid.interfaces import IIntIds

from zojax.cache.view import cache
from zojax.cache.keys import Context
from zojax.batching.batch import Batch

from zojax.contenttype.newsitem.cache import NewsItemsTag


def NewsListingBatchTag(oid, instance, *args, **kw):
    return {'bstart': (instance.news.start, len(instance.news)),
            'bpages': len(instance.news.batches),
            'context': getPath(instance.context)}


class NewsListing(object):

    def __init__(self, context, request):
        super(NewsListing, self).__init__(context, request)

        self.news = Batch(
            context.news(), size=context.pageSize, request=request)

        self.intids = getUtility(IIntIds)

    def getCategories(self, item):
        queryObject = self.intids.queryObject
        categories = []
        for uid in item.category:
            category = queryObject(uid)
            if category is not None:
                categories.append(category)
        categories.sort(key=attrgetter('title'))
        return categories

    @cache('topic.view', NewsItemsTag, NewsListingBatchTag)
    def updateAndRender(self):
        return super(NewsListing, self).updateAndRender()
