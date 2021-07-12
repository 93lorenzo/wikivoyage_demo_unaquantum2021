import pywikibot
import json
import pprint

# chose on which site we will scrape
wikivoyage_bot = pywikibot.Site('wikivoyage:it')

list_of_places = ['Riofreddo','Roviano']
#page_class = pywikibot.page.Page
template_see_text = 'Template:See'
# how the pages are defined
list_of_macro_category_templates = {
    'QuickbarWater',
    'QuickbarCity',
    'QuickbarRegion',
    'QuickbarPark',
    'QuickbarItinerary',
    'QuickbarArch',
    'QuickbarMount',
    'QuickbarDistrict',
    'QuickbarPath'
}

def retrieve_info_from_list_of_info(template_list=[],separator_elements='='):
    """
    This function retrieves info from the list (template_list)
    We assume that the each string is structured in this format 'VARIABLE=VALUE'
    :param template_list: list of elements from which we will extract info
    :param separator_elements: element that separates the value from the variable in each string of the list
    :return: curr_info_dict : dict that contains all the info retrieved
    """
    curr_info_dict = {}
    # check every element and add that to the list of dicts
    for str_elem in template_list:
        join_key = separator_elements
        key = str_elem.split(separator_elements)[0]
        list_of_values = str_elem.split(separator_elements)[1:]
        # we need to do that if there are "=" (seprators)
        # within the text
        value = separator_elements.join(list_of_values)
        curr_info_dict.update({key: value})
    return curr_info_dict

def get_info_from_places(list_of_places, list_of_macro_category_templates, separator_elements="="):
    """
    Function that print the elements of the macrocategory and the 'see' template
    ------
    :param list_of_places: list of elements to search on wikivoyage
    :param list_of_macro_category_templates: list of macrocategories used to spot the place category
    :param separator_elements: elements that separates the elements in the template list
    -------
    :return: info_dict: dict with the info of the selected places
    """
    info_dict = {}
    for place in list_of_places:
        curr_info_dict = {}
        print("*** Current place is: '{}' ***".format(place))
        # get the page of the place
        page_place = pywikibot.Page(wikivoyage_bot, place)
        # ----------------------------------------------------------------------------------------------- #
        # retrieve the page of the place as a list of tuples
        # each tuple has the first element that is a page-template element
        # ex.
        # [ (Page('Template:QuickbarCity'), ['Abitanti=742 <small>(2020)</small>', 'Altitudine=750', .... ]
        # ----------------------------------------------------------------------------------------------- #
        templates_with_params = page_place.templatesWithParams()
        # ----------------------------------------------------------------------- #
        # let's iterate on all the elements of the page!
        # we will be interested on the 'Template:QuickbarCity' element (it: città)
        # we will be interested on the 'Template:See' elements (it: cosa vedere)
        # ----------------------------------------------------------------------- #
        for current_template_tuple in templates_with_params:
            # the first element of the tuple is the page object with the template
            current_template = current_template_tuple[0]
            template_list = current_template_tuple[1]
            template_title = current_template.title()

            if template_title in list_of_macro_category_templates:
                print("This is an Example of the macro-category templates for the place  : {}\n{}".format(place,
                                                                                                          template_list))
            curr_info_dict = retrieve_info_from_list_of_info(template_list=template_list,separator_elements=separator_elements)
        # update dict
        info_dict.update({place: curr_info_dict.copy()})
    return info_dict


def print_page_category_and_see_template(list_of_places, list_of_macro_category_templates):
    """
    Function that print the elements of the macrocategory and the 'see' template. It also returns a dict with the info of see template
    ------
    :param list_of_places: list of elements to search on wikivoyage
    :param list_of_macro_category_templates: list of macrocategories used to spot the place category
    -------
    :return: info_dict that contains all the template see info for the place
    """
    info_dict = {}
    separator_elements = '='
    for place in list_of_places:
        template_see_text_list_dict = []
        print("*** Current place is: '{}' ***".format(place))
        # get the page of the place
        page_place = pywikibot.Page(wikivoyage_bot, place)
        # ----------------------------------------------------------------------------------------------- #
        # retrieve the page of the place as a list of tuples
        # each tuple has the first element that is a page-template element
        # ex.
        # [ (Page('Template:QuickbarCity'), ['Abitanti=742 <small>(2020)</small>', 'Altitudine=750', .... ]
        # ----------------------------------------------------------------------------------------------- #
        templates_with_params = page_place.templatesWithParams()
        # ----------------------------------------------------------------------- #
        # let's iterate on all the elements of the page!
        # we will be interested on the 'Template:QuickbarCity' element (it: città)
        # we will be interested on the 'Template:See' elements (it: cosa vedere)
        # ----------------------------------------------------------------------- #
        for current_template_tuple in templates_with_params:
            # the first element of the tuple is the page object with the template
            current_template = current_template_tuple[0]
            template_list = current_template_tuple[1]
            template_title = current_template.title()

            if template_title == template_see_text:
                print("This is an Example of 'See' template for the place : {}\n{}".format(place, template_list))
                curr_info_dict = retrieve_info_from_list_of_info(template_list=template_list,
                                                                 separator_elements=separator_elements)
                # append see template
                template_see_text_list_dict.append(curr_info_dict.copy())

            if template_title in list_of_macro_category_templates:
                print("This is an Example of the macro-category templates for the place  : {}\n{}".format(place,
                                                                                                          template_list))
        info_dict.update({place: template_see_text_list_dict })
    return info_dict
if __name__ == '__main__':
    print("Example of getting info from the macrocategory")

    info_dict = get_info_from_places(list_of_places=list_of_places,
                                     list_of_macro_category_templates=list_of_macro_category_templates)
    pprint.pprint(info_dict)
    json_file_info = "info.json"
    print("Saving the info about the places into json file : {}".format(json_file_info))
    with open(json_file_info, 'w') as fp:
        json.dump(info_dict, fp)

    print("Example of print see template and macrocategory")
    info_dict_see_template = print_page_category_and_see_template(list_of_places=list_of_places,
                                         list_of_macro_category_templates=list_of_macro_category_templates)
    json_file_info_see_template = "info_see_template.json"
    print("Saving the info about the places into json file : {}".format(json_file_info_see_template))
    with open(json_file_info_see_template, 'w') as fp:
        json.dump(info_dict_see_template, fp)

