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
"""Porlet interfaces

$Id$
"""
from zope import interface, schema
from zojax.contenttypes.interfaces import _
from zojax.widget.checkbox.field import CheckboxList


class INewsItemsPortlet(interface.Interface):
    """ news items portlet """

    label = schema.TextLine(
        title = _(u'Label'),
        required = False)

    number = schema.Int(
        title = _(u'Number of news items'),
        default = 7,
        required = True)

    categories = CheckboxList(
        title = _(u'Categories'),
        description = _('Filter news items by their category. '
                        'If no category selected, no filtering '
                        'will be performed.'),
        vocabulary = 'zojax.contenttype.newsitem-portal-categories',
        default = [],
        required = False)

    source = schema.Choice(
        title = _(u'News source'),
        vocabulary='newsitem.portlet.sources',
        default = 2)

class INewsCategoriesPortlet(interface.Interface):
    """ news category listing portlet """
