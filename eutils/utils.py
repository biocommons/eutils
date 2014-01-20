def xml_get1(node,xpath):
    return node.xpath(xpath)[0]

def xml_get1_or_none(node,xpath):
    try:
        return xml_get1(node,xpath)
    except IndexError:
        return None

def xml_get_text(node,xpath):
    return xml_get1(node,xpath).text

def xml_get_text_or_none(node,xpath):
    try:
        return xml_get_text(node,xpath)
    except IndexError:          # xpath search found 0 matches
        return None


def xml_xpath_text(node,xpath):
    return [ n.text for n in node.xpath(xpath) ]
def xml_xpath_text_first(node,xpath):
    try: 
        return xml_xpath_list_text(node,xpath)[0]
    except IndexError:
        return None


def arglist_to_dict(**args):
    return dict(**args)
a2d = arglist_to_dict
