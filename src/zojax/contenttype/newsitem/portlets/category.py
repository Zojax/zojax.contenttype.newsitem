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
"""News categories portlet

$Id$
"""
from zope import interface
from zope.component import queryUtility
from zope.app.component.hooks import getSite
from zojax.catalog.interfaces import ICatalog

from interfaces import INewsCategoriesPortlet


class NewsCategoriesPortlet(object):
    interface.implements(INewsCategoriesPortlet)

    categories = None

    def update(self):
        super(NewsCategoriesPortlet, self).update()
        site = getSite()
        catalog = queryUtility(ICatalog)
        if catalog is not None:
            query = dict(
                searchContext=(site,),
                type={'any_of': ('contenttype.newsitem.category',)}
                )
            self.categories = catalog.searchResults(**query)

    def isAvailable(self):
        if not self.categories:
            return False
        return super(NewsCategoriesPortlet, self).isAvailable()
