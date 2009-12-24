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
from zope.proxy import removeAllProxies
from zope.component import getUtility, queryAdapter
from zope.lifecycleevent import ObjectCreatedEvent
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.app.component.hooks import getSite
from zope.app.component.interfaces import ISite
from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.intid.interfaces import IIntIds

from zojax.catalog.interfaces import ICatalog
from zojax.content.draft.interfaces import IDraftContent
from zojax.content.space.interfaces import ISpace, IWorkspaceFactory
from zojax.content.type.item import PersistentItem
from zojax.content.type.container import ContentContainer
from zojax.content.type.interfaces import ISearchableContent

from interfaces import _, \
    ICategory, ICategoryContainer, INewsWorkspace, INewsItem


class Category(PersistentItem):
    interface.implements(ICategory, ISearchableContent)


class CategoryContainer(ContentContainer):
    interface.implements(ICategoryContainer)

    title = _(u'Categories')


@interface.implementer(IVocabularyFactory)
def CategoryIdsVocabulary(context):

    while True:
        if ISpace.providedBy(context):
            break

        if IDraftContent.providedBy(context):
            context = context.getLocation()
            if context is not None:
                context = context.__parent__
            break

        context = getattr(context, '__parent__', None)
        if context is None:
            break

    if context is None:
        return SimpleVocabulary(())

    getId = getUtility(IIntIds).getId
    terms = []

    while True:
        wf = queryAdapter(context, IWorkspaceFactory, name='news')
        if wf is not None and wf.isInstalled():
            for category in context['news']['category'].values():
                id = getId(removeAllProxies(category))
                term = SimpleTerm(id, str(id), category.title)
                term.description = category.description
                terms.append((term.title, term))

        if ISite.providedBy(context):
            break

        context = getattr(context, '__parent__', None)
        if context is None or not ISpace.providedBy(context):
            break

    terms.sort()
    return SimpleVocabulary([term for _t, term in terms])


@interface.implementer(IVocabularyFactory)
def PortalCategoryIdsVocabulary(context=None):
    result = getUtility(ICatalog).searchResults(
        type={'any_of': ('contenttype.newsitem.category', )})
    getObject = result.uidutil.getObject

    terms = []

    for uid in result.uids:
        category = getObject(uid)
        term = SimpleTerm(uid, str(uid), category.title)
        term.description = category.description
        terms.append((term.title, term))

    terms.sort()
    return SimpleVocabulary([term for _t, term in terms])
