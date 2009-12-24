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
import time, rfc822
from zope import interface, component
from zope.component import getUtility
from zope.traversing.browser import absoluteURL

from zojax.content.feeds.rss2 import RSS2Feed
from zojax.catalog.interfaces import ICatalog
from zojax.ownership.interfaces import IOwnership
from zojax.content.space.interfaces import ISpace
from zojax.principal.profile.interfaces import IPersonalProfile

from interfaces import _, INewsRssFeed, INewsWorkspace


class NewsRssFeed(RSS2Feed):
    component.adapts(ISpace)
    interface.implementsOnly(INewsRssFeed)

    name = u'news'
    title = _(u'News')
    description = _(u'Information about latest site news.')

    def items(self):
        request = self.request
        catalog = getUtility(ICatalog)

        results = catalog.searchResults(
            searchContext=(self.context,),
            sort_on='effective', sort_order='reverse',
            draftContent = {'any_of': (False,)},
            typeType = {'any_of': ('News Item',)})[:15]

        for item in results:
            url = absoluteURL(item, request)

            info = {
                'title': item.title,
                'description': item.description,
                'guid': '%s/'%url,
                'pubDate': rfc822.formatdate(time.mktime(item.date.timetuple())),
                'isPermaLink': True}

            principal = IOwnership(item).owner
            if principal is not None:
                profile = IPersonalProfile(principal)
                info['author'] = u'%s (%s)'%(profile.email, profile.title)

            yield info


class NewsWorkspaceRssFeed(RSS2Feed):
    component.adapts(INewsWorkspace)
    interface.implementsOnly(INewsRssFeed)

    name = u'news'
    title = _(u'News')
    description = _(u'Information about latest site news.')

    def items(self):
        request = self.request

        for item in self.context.news()[:15]:
            url = absoluteURL(item, request)

            info = {
                'title': item.title,
                'description': item.description,
                'guid': '%s/'%url,
                'pubDate': rfc822.formatdate(time.mktime(item.date.timetuple())),
                'isPermaLink': True}

            principal = IOwnership(item).owner
            if principal is not None:
                profile = IPersonalProfile(principal)
                info['author'] = u'%s (%s)'%(profile.email, profile.title)

            yield info
