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

