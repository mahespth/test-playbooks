import pytest
from common.ui.pages import Login_Page, Portal_Page


@pytest.fixture
def ui_login_pg(mozwebqa):
    '''Logs in to the application with default credentials and returns the
    home page'''
    login_pg = Login_Page(mozwebqa)
    return login_pg.go_to_login_page()


@pytest.fixture
def home_page_logged_in(ui_login_pg):
    '''Logs in to the application with default credentials and returns the
    home page'''
    home_pg = ui_login_pg.login()
    assert home_pg.is_logged_in, 'Unable to determine if logged in'
    return home_pg


@pytest.fixture
def ui_dashboard_pg(home_page_logged_in):
    '''Navigate to the Home tab and return it'''
    if home_page_logged_in.is_the_dashboard_page:
        return home_page_logged_in
    else:
        return home_page_logged_in.main_menu.click('Home')


@pytest.fixture
def ui_portal_pg(request, mozwebqa):
    '''Navigate to Portal Mode and return the corresponding page object.'''
    # TODO - support overriding the login via a pytest marker
    # This isn't well used or tested at the moment, but it would be nice to
    # have a generic mechanism for returning a page object, without logging in.
    fixture_args = getattr(request.function, 'fixture_args', None)
    if fixture_args is None or fixture_args.kwargs.get('login', True):
        home_page_logged_in = request.getfuncargvalue('home_page_logged_in')
        return home_page_logged_in.account_menu.click('Portal Mode')
    else:
        obj = Portal_Page(mozwebqa)
        obj.open("/#/portal")
        return obj


@pytest.fixture
def ui_organizations_pg(home_page_logged_in):
    '''Navigate to the Organizations tab and return it'''
    return home_page_logged_in.main_menu.click('Organizations')


@pytest.fixture
def ui_users_pg(home_page_logged_in):
    '''Navigate to the Users tab and return it'''
    return home_page_logged_in.main_menu.click('Users')


@pytest.fixture
def ui_teams_pg(home_page_logged_in):
    '''Navigate to the Teams tab and return it'''
    return home_page_logged_in.main_menu.click('Teams')


@pytest.fixture
def ui_credentials_pg(home_page_logged_in):
    '''Navigate to the Credentials tab and return it'''
    return home_page_logged_in.main_menu.click('Credentials')


@pytest.fixture
def ui_projects_pg(home_page_logged_in):
    '''Navigate to the Projects tab and return it'''
    return home_page_logged_in.main_menu.click('Projects')


@pytest.fixture
def ui_inventories_pg(home_page_logged_in):
    '''Navigate to the Inventories tab and return it'''
    return home_page_logged_in.main_menu.click('Inventories')


@pytest.fixture
def ui_job_Templates_pg(home_page_logged_in):
    '''Navigate to the Job_Templates tab and return it'''
    return home_page_logged_in.main_menu.click('Job Templates')


@pytest.fixture
def ui_jobs_pg(home_page_logged_in):
    '''Navigate to the Jobs tab and return it'''
    return home_page_logged_in.main_menu.click('Jobs')
