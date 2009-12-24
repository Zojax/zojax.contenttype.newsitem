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
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.app.intid.interfaces import IIntIds
from zope.traversing.api import getParents
from zope.traversing.interfaces import IContainmentRoot

from zojax.catalog.interfaces import ICatalog
from zojax.content.type.interfaces import IItem, IContent, IContentContainer

from interfaces import _


def sourcesVocabulary(context):
    return SimpleVocabulary((
        SimpleTerm(1, '1', _(u'Current space')),
        SimpleTerm(2, '2', _(u'Current space and subspaces')),
        SimpleTerm(3, '3', _(u"All spaces")),
        ))
