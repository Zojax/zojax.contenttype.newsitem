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
"""News item view

$Id$
"""
from operator import attrgetter
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds


class NewsItemPage(object):

    def update(self):
        queryObject = getUtility(IIntIds).queryObject
        self.categories = categories = []
        for uid in self.context.category:
            category = queryObject(uid)
            if category is not None:
                categories.append(category)
        categories.sort(key=attrgetter('title'))
