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
""" news item interfaces

$Id$
"""
from zope import schema, interface
from zojax.content.type.interfaces import IItem
from zojax.richtext.field import RichText
from zojax.widget.checkbox.field import CheckboxList
from zojax.contenttypes.interfaces import _
from zojax.content.feeds.interfaces import IRSS2Feed
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory


class INewsItem(IItem):
    """ news item """

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'News item title.'),
        required = True)

    description = schema.Text(
        title = _(u'Description'),
        description = _(u'News item description.'),
        required = False)

    date = schema.Datetime(
        title = _(u'Date'),
        description = _(u'News date'),
        required = True)

    text = RichText(
        title = _(u'Body'),
        description = _(u'News item text.'),
        required = True)

    category = CheckboxList(
        title = _(u'Category'),
        description = _('Select category for the news item.'),
        vocabulary = 'zojax.contenttype.newsitem-categories',
        default = [],
        required = False)


class ICategory(IItem):
    """ news item category """


class ICategoryContainer(interface.Interface):
    """ news item category container """


class INewsItemType(interface.Interface):
    """ news item content type marker interface """


class INewsWorkspace(IWorkspace):
    """ news workspace """

    pageSize = schema.Int(
        title = _(u'Page size'),
        description = _(u'Number of news items per page.'),
        default = 15,
        required = True)

    subspaces = schema.Bool(
        title = _(u'Sub spaces'),
        description = _(u'Show news for all sub-spaces or just for current space.'),
        default = False,
        required = True)

    def news(categories=None):
        """ list news items

        categories argument is a set of category IDs that can be passed
        to filter news items.
        """


class INewsWorkspaceFactory(IWorkspaceFactory):
    """ news workspace factory """


class INewsRssFeed(IRSS2Feed):
    """ news rss feed """
