from collections import OrderedDict
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, _
from odoo.http import request, route
from odoo.exceptions import AccessError, MissingError
from odoo.osv.expression import AND


class EaglePortal(CustomerPortal):

    def _get_properties_portal_domain(self):
        return [
            ('is_published', '=', True)
        ]

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        values['properties_count'] = 0
        if 'properties_count' in counters:
            domain = self._get_properties_portal_domain()
            values['properties_count'] = request.env['eagle.property'].sudo().search_count(domain)
        return values

    def _get_properties_searchbar_filters(self):
        return {
            'all': {'label': _('All'), 'domain': []},
            'invoices': {'label': _('Compounds'), 'domain': [('parent_id', '=', False)]},
            'bills': {'label': _('Units'), 'domain': [('parent_id', '!=', False)]},
        }

    def _prepare_my_properties_values(self, page, date_begin, date_end, sortby, filterby, domain=None,
                                      url="/my/properties"):
        values = self._prepare_portal_layout_values()
        EagleProperty = request.env['eagle.property']
        domain = AND([
            domain or [],
            self._get_properties_portal_domain(),
        ])
        # On the list view of published properties, we want to allow the user to sort and filter the properties
        # based on pre-defined options. We define these options in the following dictionaries.
        # - searchbar_sortings for the sorting options
        searchbar_sortings = {
            'construction_date': {'label': _('Construction Date'), 'order': 'construction_date desc'},
            'surface': {'label': _('Surface Area'), 'order': 'surface desc'},
        }
        # - searchbar_filters for the filtering options
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'invoices': {'label': _('Compounds'), 'domain': [('parent_id', '=', False)]},
            'bills': {'label': _('Units'), 'domain': [('parent_id', '!=', False)]},
        }
        # default sort by order
        if not sortby:
            sortby = 'construction_date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        values.update({
            'date': date_begin,
            # content according to pager and archive selected
            # lambda function to get the invoices recordset when the pager will be defined in the main method of a route
            'properties': lambda pager_offset: (
                EagleProperty.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
                if EagleProperty.check_access_rights('read', raise_exception=False) else
                EagleProperty
            ),
            'page_name': 'property',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                "total": EagleProperty.search_count(domain) if EagleProperty.check_access_rights('read',
                                                                                                 raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return values

    @route(['/my/properties', '/my/properties/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_properties(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        # First, we get the initial values required for the portal layout
        # This includes: sales_user & page_name
        values = self._prepare_portal_layout_values()
        # We defined a method that returns the domain applied when fetching properties for the portal
        domain = self._get_properties_portal_domain()
        EagleProperty = request.env['eagle.property']
        # On the list view of published properties, we want to allow the user to sort and filter the properties
        # based on pre-defined options. We define these options in the following dictionaries.
        # - searchbar_sortings for the sorting options
        searchbar_sortings = {
            'construction_date': {'label': _('Construction Date'), 'order': 'construction_date desc'},
            'surface': {'label': _('Surface Area'), 'order': 'surface desc'},
        }
        # - searchbar_filters for the filtering options
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'invoices': {'label': _('Compounds'), 'domain': [('parent_id', '=', False)]},
            'bills': {'label': _('Units'), 'domain': [('parent_id', '!=', False)]},
        }
        # default sort by order
        if not sortby:
            sortby = 'construction_date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        # Prepare the pager values for pagination
        pager = portal_pager(
            url="/my/properties",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby},
            total=EagleProperty.search_count(domain),
            page=page,
            step=self._items_per_page
        )
        # Search the properties that will be printed on the web page
        properties = EagleProperty.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_properties_history'] = properties.ids[:100]
        # Update the values dict
        values.update({
            'date': date_begin,
            'properties': properties,
            'page_name': 'property',
            'pager': pager,
            'default_url': "/my/properties",
            'searchbar_sortings': searchbar_sortings,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'sortby': sortby,
            'filterby': filterby,
        })
        # Once we have prepared all the required values, we then render the QWeb template
        return request.render("eagle_estates.portal_my_properties", values)

    @route('/my/properties/<int:property_id>', type='http', auth="user", website=True)
    def portal_my_property(self, property_id, access_token=None, **kw):
        try:
            property_sudo = self._document_check_access('eagle.property', property_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = {
            'page_name': 'property',
            'property_id': property_sudo,
        }
        values = self._get_page_view_values(
            property_sudo, access_token, values, 'my_properties_history', False, **kw
        )
        return request.render("eagle_estates.portal_my_property", values)
