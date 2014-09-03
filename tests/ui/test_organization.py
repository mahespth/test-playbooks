import pytest
import common.utils
from tests.ui import Base_UI_Test


@pytest.fixture(scope="function")
def table_sort(request, admin_user, org_admin):
    return [('name', 'ascending'),
            ('name', 'descending'),
            ('description', 'ascending'),
            ('description', 'descending')]


@pytest.fixture(scope="function")
def many_organizations_count(request):
    return 55


@pytest.fixture(scope="function")
def many_organizations(request, authtoken, api_organizations_pg, many_organizations_count):

    obj_list = list()
    for i in range(many_organizations_count):
        payload = dict(name="org %s %s" % (common.utils.random_unicode(), i),
                       description="Random organization %s %s" % (common.utils.random_unicode(), i))
        obj = api_organizations_pg.post(payload)
        request.addfinalizer(obj.delete)
        obj_list.append(obj)
    return obj_list


@pytest.mark.selenium
@pytest.mark.nondestructive
class Test_Organization(Base_UI_Test):

    pytestmark = pytest.mark.usefixtures('maximized', 'backup_license', 'install_license_unlimited')

    def test_active_tab(self, ui_organizations_pg):
        '''Verify the basics of the organizations page'''
        assert ui_organizations_pg.is_the_active_tab

        # FIXME - assert 'organizations' table is visible (id=organizations_table)
        # FIXME - assert 'organizations' search box is visible (id=search-widget-container)

    def test_activity_stream(self, ui_organizations_pg):
        '''Verify that the organization activity stream can be open and closed'''
        # Open activity_stream
        orgs_activity_pg = ui_organizations_pg.activity_stream_btn.click()
        assert orgs_activity_pg.is_the_active_tab
        assert orgs_activity_pg.is_the_active_breadcrumb

        # Refresh activity_stream
        orgs_activity_pg.refresh_btn.click()

        # Close activity_stream
        ui_organizations_pg = orgs_activity_pg.close_btn.click()
        assert ui_organizations_pg.is_the_active_tab

    def test_sort(self, many_organizations, table_sort, ui_organizations_pg):
        '''Verify organiation table sorting'''
        assert ui_organizations_pg.is_the_active_tab

        # Verify default table sort column
        assert ui_organizations_pg.table.sorted_by == 'name', \
            "Unexpected default table sort column (%s != %s)" % \
            (ui_organizations_pg.table.sorted_by, 'name')

        # Verify default table sort order
        assert ui_organizations_pg.table.sort_order == 'ascending', \
            "Unexpected default table sort order (%s != %s)" % \
            (ui_organizations_pg.table.sort_order, 'ascending')

        for sorted_by, sort_order in table_sort:
            # Change table sort
            ui_organizations_pg.table.sort_by(sorted_by, sort_order)

            # Verify new table sort column
            assert ui_organizations_pg.table.sorted_by == sorted_by, \
                "Unexpected default table sort column (%s != %s)" % \
                (ui_organizations_pg.table.sorted_by, sorted_by)

            # Verify new table sort order
            assert ui_organizations_pg.table.sort_order == sort_order, \
                "Unexpected default table sort order (%s != %s)" % \
                (ui_organizations_pg.table.sort_order, sort_order)

    def test_no_pagination(self, authtoken, api_organizations_pg, api_default_page_size, ui_organizations_pg):
        '''Verify organiation table pagination is not present'''

        if api_organizations_pg.get().count > api_default_page_size:
            pytest.skip("Unable to test as too many organizations exist")

        assert not ui_organizations_pg.pagination.is_displayed(), \
            "Pagination present, but fewer than %d organizations are visible" % \
            api_default_page_size

    def test_pagination(self, many_organizations, ui_organizations_pg):
        '''Verify organiation table pagination'''

        assert ui_organizations_pg.pagination.is_displayed(), "Unable to find pagination"

        # TODO: Verify expected number of items in pagination

        # Assert expected pagination links
        assert ui_organizations_pg.pagination.current_page == 1, \
            "Unexpected current page number (%d != %d)" % \
            (ui_organizations_pg.pagination.current_page, 1)
        assert not ui_organizations_pg.pagination.first_page.is_displayed()
        assert not ui_organizations_pg.pagination.prev_page.is_displayed()
        assert ui_organizations_pg.pagination.next_page.is_displayed()
        assert not ui_organizations_pg.pagination.last_page.is_displayed()
        assert ui_organizations_pg.pagination.count == 3, \
            "Unexpected number of pagination links (%d != %d)" % \
            (ui_organizations_pg.pagination.count, 3)

        # Click next_page
        next_pg = ui_organizations_pg.pagination.next_page.click()

        # Assert expected pagination links
        assert next_pg.pagination.current_page == 2, \
            "Unexpected current page number (%d != %d)" % \
            (next_pg.pagination.current_page, 2)
        assert not next_pg.pagination.first_page.is_displayed()
        assert next_pg.pagination.prev_page.is_displayed()
        assert next_pg.pagination.next_page.is_displayed()
        assert not next_pg.pagination.last_page.is_displayed()
        assert next_pg.pagination.count == 3, \
            "Unexpected number of pagination links (%d != %d)" % \
            (next_pg.pagination.count, 3)

        # Click next_page
        last_pg = next_pg.pagination.next_page.click()

        # Assert expected pagination links
        assert last_pg.pagination.current_page == 3, \
            "Unexpected current page number (%d != %d)" % \
            (last_pg.pagination.current_page, 3)
        assert not last_pg.pagination.first_page.is_displayed()
        assert last_pg.pagination.prev_page.is_displayed()
        assert not last_pg.pagination.next_page.is_displayed()
        assert not last_pg.pagination.last_page.is_displayed()
        assert last_pg.pagination.count == 3, \
            "Unexpected number of pagination links (%d != %d)" % \
            (last_pg.pagination.count, 3)

    def test_filter(self, organization, ui_organizations_pg):
        '''Verify organiation table filtering'''
        assert ui_organizations_pg.is_the_active_tab

        # search by name
        ui_organizations_pg.search.search_type_btn.click()
        ui_organizations_pg.search.search_type_options.get("Name").click()
        # FIXME - assert the selected search_type == "Name"
        ui_organizations_pg.search.search_value = organization.name
        ui_organizations_pg = ui_organizations_pg.search.search_btn.click()

        # TODO: verify expected number of items found
        # assert ui_organizations_pg.pagination.total_items == 1
        num_rows = len(list(ui_organizations_pg.table.rows))
        assert num_rows == 1, "Unexpected number of results found (%d != %d)" % (num_rows, 1)

        # search by description
        ui_organizations_pg.search.search_type_btn.click()
        ui_organizations_pg.search.search_type_options.get("Description").click()
        # FIXME - assert the selected search_type == "Description"
        ui_organizations_pg.search.search_value = organization.description
        ui_organizations_pg = ui_organizations_pg.search.search_btn.click()

        # TODO: verify expected number of items found
        # assert ui_organizations_pg.pagination.total_items == 1
        num_rows = len(list(ui_organizations_pg.table.rows))
        assert num_rows == 1, "Unexpected number of results found (%d != %d)" % (num_rows, 1)

        # reset search filter
        ui_organizations_pg = ui_organizations_pg.search.reset_btn.click()
        assert ui_organizations_pg.search.search_value == '', \
            "search_value did not reset (%s)" % \
            ui_organizations_pg.search.search_value

    def test_add(self, ui_organizations_pg):
        '''Verify basic organiation form fields'''
        assert ui_organizations_pg.add_btn, "Unable to locate add button"

        # Click Add button
        add_pg = ui_organizations_pg.add_btn.click()
        assert add_pg.is_the_active_tab
        assert add_pg.is_the_active_breadcrumb

        # Input Fields
        add_pg.name = "Random Organization - %s" % common.utils.random_unicode()
        add_pg.description = "Random description - %s" % common.utils.random_unicode()

        # Click Reset
        add_pg.reset_btn.click()
        assert add_pg.name == "", "Reset button did not reset the field: name"
        assert add_pg.description == "", "Reset button did not reset the field: description"

    def test_accordions(self, ui_organizations_pg, organization):
        '''Verify the organiation accordions behave properly'''
        # Open edit page
        edit_pg = ui_organizations_pg.open(organization.id)
        assert edit_pg.is_the_active_tab
        assert edit_pg.is_the_active_breadcrumb

        # Assert default collapsed accordions
        assert edit_pg.accordion.get('Properties')[0].is_expanded(), "The properties accordion was not expanded as expected"
        assert edit_pg.accordion.get('Users')[0].is_collapsed(), "The users accordion was not collapsed as expected"
        assert edit_pg.accordion.get('Administrators')[0].is_collapsed(), "The administrators accordion was not collapsed as expected"

        # Expand the Users accordion
        edit_pg.accordion.get('Users')[0].expand()
        assert edit_pg.accordion.get('Properties')[0].is_collapsed(), "The properties accordion was not collapse as expected"
        assert edit_pg.accordion.get('Users')[0].is_expanded(), "The users accordion was not expand as expected"
        assert edit_pg.accordion.get('Administrators')[0].is_collapsed(), "The administrators accordion was not collapse as expected"

        # Re-open edit page and verify accordion memory
        edit_pg = ui_organizations_pg.open(organization.id)
        assert edit_pg.is_the_active_tab
        assert edit_pg.accordion.get('Properties')[0].is_collapsed(), "The properties accordion was not collapse as expected"
        assert edit_pg.accordion.get('Users')[0].is_expanded(), "The users accordion was not expand as expected"
        assert edit_pg.accordion.get('Administrators')[0].is_collapsed(), "The administrators accordion was not collapse as expected"

    def test_edit_properties(self, ui_organizations_pg, organization):
        '''Verify basic organiation form fields when editing an organization'''
        edit_pg = ui_organizations_pg.open(organization.id)
        assert edit_pg.is_the_active_tab
        assert edit_pg.is_the_active_breadcrumb

        # Access the edit region
        edit_region = edit_pg.accordion.get('Properties')[1]

        # Modify organization form fields
        edit_region.name = common.utils.random_unicode()
        edit_region.description = common.utils.random_unicode()

        # Verify breadcrumb title updated
        assert edit_pg.is_the_active_breadcrumb

        # Reset Edit form
        edit_region.reset_btn.click()
        assert edit_pg.is_the_active_breadcrumb
        assert edit_region.name == organization.name, \
            "The reset button did not restore the 'name' (%s != %s)" % \
            (edit_region.name, organization.name)
        assert edit_region.description == organization.description, \
            "The reset button did not restore the 'description' (%s != %s)" % \
            (edit_region.description, organization.description)

    def test_edit_users(self, ui_organizations_pg, organization):
        '''Verify basic operation of organizations users accordion'''
        edit_pg = ui_organizations_pg.open(organization.id)
        # Access the users region
        (users_header, users_region) = edit_pg.accordion.get('Users')
        users_header.expand()
        org_users_pg = users_region.add_btn.click()
        assert org_users_pg.is_the_active_tab
        assert org_users_pg.is_the_active_breadcrumb

    def test_edit_admins(self, ui_organizations_pg, organization):
        '''Verify basic operation of organizations admins accordion'''

        edit_pg = ui_organizations_pg.open(organization.id)
        # Access the users region
        (users_header, users_region) = edit_pg.accordion.get('Administrators')
        users_header.expand()
        org_users_pg = users_region.add_btn.click()
        assert org_users_pg.is_the_active_tab
        assert org_users_pg.is_the_active_breadcrumb


# @pytest.mark.selenium
# @pytest.mark.nondestructive
# class Test_Organization_LowRes(Base_UI_Test):
