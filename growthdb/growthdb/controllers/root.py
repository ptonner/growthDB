# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from growthdb import model
from growthdb.controllers.secure import SecureController
from growthdb.model import DBSession, ExperimentalDesign
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from growthdb.lib.base import BaseController
from growthdb.controllers.error import ErrorController

from growthdb.model.strain import Strain

__all__ = ['RootController']

# import tw2.core as twc
# import tw2.forms as twf

# class MovieForm(twf.Form):
#     class child(twf.TableLayout):
#         title = twf.TextField()
#         director = twf.TextField(value='Default Director')
#         genres = twf.CheckBoxList(options=['Action', 'Comedy', 'Romance', 'Sci-fi'])

#     action = '/save_movie'

from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm
from sprox.widgets import PropertySingleSelectField

class StrainTableFiller(TableFiller):
    __model__ = Strain

    def children(self, obj):
       # print 'obj:',obj
       children = ', '.join(['<a href="/strain/'+str(d.gene)+'">'+d.gene+'</a>'
                              for d in obj.children])
       return children.join(('<div>', '</div>'))

    def parent(self, obj):
       # print 'obj:',obj
       # parent = DBSession
       # children = ', '.join(['<a href="/strain/'+str(d.gene)+'">'+d.gene+'</a>'
       #                        for d in obj.children])
       parent = ""
       if not obj.parent is None:
           parent = '<a href="/strain/'+str(obj.parent.gene)+'">'+obj.parent.gene+'</a>'
       return parent.join(('<div>', '</div>'))

strain_table_filler = StrainTableFiller(DBSession)

class StrainTable(TableBase):
    __model__ = Strain
    __omit_fields__ = ['id','parent_id']
    __xml_fields__ = ['children','parent']
strain_table = StrainTable(DBSession)

class StrainAddForm(AddRecordForm):
    __model__ = Strain
    __omit_fields__ = ['id','experimental_designs','parent_id','children']
    __dropdown_field_names__ = {'parent':'gene'}
    # __field_attrs__ = {'gene':{'rows':'2'}}
    
strain_add_form = StrainAddForm(DBSession)


class StrainController(CrudRestController):
    model = Strain
    table = strain_table
    table_filler = strain_table_filler
    new_form = strain_add_form

# class RootController(BaseController):
    # movie = MovieController(DBSession)


class RootController(BaseController):
    """
    The root controller for the growthdb application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    strain = StrainController(DBSession)

    def _before(self, *args, **kw):
        tmpl_context.project_name = "growthdb"

    @expose('growthdb.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    # @expose('growthdb.templates.strain')
    # def strain(self,pagename="nrc1"):
    #     """Handle the strain-page."""
    #     from sqlalchemy.exc import InvalidRequestError

    #     try:
    #         strain = DBSession.query(Strain).filter_by(gene=pagename).one()
    #     except InvalidRequestError:
    #         raise redirect("strainnotfound", pagename=pagename)

    #     # strain = DBSession.query(Strain).filter_by(gene=pagename).one()
    #     # print "strain:", strain
    #     # print "parent:",strain.parent
    #     # # parent = DBSession.query(Strain).filter_by(id=strain.parent).one()
    #     return dict(strain=strain)

    @expose('growthdb.templates.editstrain')
    def strainedit(self, *args, **kw):
        return dict(page='nrc1', form=MovieForm)

    @expose('growthdb.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('growthdb.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

    @expose('growthdb.templates.data')
    @expose('json')
    def data(self, **kw):
        """
        This method showcases how you can use the same controller
        for a data page and a display page.
        """
        return dict(page='data', params=kw)

    @expose('growthdb.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('growthdb.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('growthdb.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if failure is not None:
            if failure == 'user-not-found':
                flash(_('User not found'), 'error')
            elif failure == 'invalid-password':
                flash(_('Invalid Password'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)
