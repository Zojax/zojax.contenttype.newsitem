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
from zope.security import checkPermission
from zope.traversing.browser import absoluteURL
from zojax.content.actions.action import Action
from zojax.content.space.interfaces import IContentSpace
from zojax.content.actions.interfaces import IAction, IContextAction
from zojax.contenttype.newsitem.interfaces import _, INewsWorkspace


class IRSSNewsItemsAction(IContextAction):
    pass


class RSSNewsItemsAction(Action):
    interface.implements(IRSSNewsItemsAction)
    component.adapts(INewsWorkspace, interface.Interface)

    weight = 99999
    title = _(u'News rss feed')

    @property
    def url(self):
        return '%s/@@feeds/news'%(absoluteURL(self.context, self.request))

    def isAvailable(self):
        return True
