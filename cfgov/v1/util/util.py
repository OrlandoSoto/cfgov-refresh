import collections
import re
from itertools import chain
from time import time
from django.conf import settings
from wagtail.wagtailcore.blocks.stream_block import StreamValue
from wagtail.wagtailcore.blocks.struct_block import StructValue


def id_validator(id_string, search=re.compile(r'[^a-zA-Z0-9-_]').search):
    if id_string:
        return not bool(search(id_string))
    else:
        return False


# example_case ==> ExampleCase
def to_camel_case(snake_str):
    snake_str = snake_str.capitalize()
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])


def get_unique_id(prefix='', suffix=''):
    index = hex(int(time()*10000000))[2:]
    return prefix + str(index) + suffix


 # These messages are manually mirrored on the
 # Javascript side in error-messages-config.js
ERROR_MESSAGES = {
    'CHECKBOX_ERRORS' : {
        'required' : 'Please select at least one of the "%s" options.'
    },
    'DATE_ERRORS' :{
        'invalid' : 'You have entered an invalid date.',
        'one_required': 'Please enter at least one date.'
    }
}


# Orders by most to least common in the given list.
def most_common(lst):
    # Returns the lst if empty or there's just one element in it.
    if not lst or len(lst) == 1:
        return lst
    else:
        # Gets the most common element in the list.
        most = max(set(lst), key=lst.count)
        # Creates a new list without that element.
        new_list = [e for e in lst if most not in e]
        # Recursively returns a list with the most common elements ordered
        # most to least. Ties go to the lowest index in the given list.
        return [most] + most_common(new_list)


def get_form_id(page, get_request):
        form_ids = []
        if callable(getattr(page, 'get_form_specific_filter_data', None)):
            form_ids = page.get_form_specific_filter_data(page.get_form_class(),
                                                          get_request).keys()
        if form_ids:
            return form_ids[0]
        else:
            return None


# For use by Browse type pages to get the secondary navigation items
def get_secondary_nav_items(current):
    from ..templatetags.share import get_page_state_url
    nav_items = []
    parent = current.get_parent()
    page = parent if 'Browse' in parent.specific_class.__name__ else current
    # Use chain to add the page object in from the function call since the page
    # argument passed could be difference than the one in the database.
    for sibling in list(chain([page], page.get_siblings(inclusive=False))):
        # Only if it's a Browse type page
        if 'Browse' in sibling.specific_class.__name__:
            item = {
                'title': sibling.title,
                'slug': sibling.slug,
                'url': get_page_state_url({}, sibling),
                'order': sibling.specific.secondary_nav_order,
                'children': [],
            }
            for child in list(chain([sibling], sibling.get_siblings(inclusive=False))):
                if 'Browse' in child.specific_class.__name__:
                    item['children'].append({
                        'title': child.title,
                        'slug': child.slug,
                        'url': get_page_state_url({}, child),
                        'order': child.specific.secondary_nav_order,
                    })
            item['children'] = sorted(item['children'], key=lambda x: x['order'])
            nav_items.append(item)
    # Return a boolean about whether or not the current page has Browse children
    nav_items = sorted(nav_items, key=lambda x: x['order'])
    for item in nav_items:
        if get_page_state_url({}, page) == item['url'] and item['children']:
            return nav_items, True
    return nav_items, False
