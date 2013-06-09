def xml_get_text(node,xpath):
    return node.xpath(xpath)[0].text

def xml_get_text_or_none(node,xpath):
    try:
        return xml_get_text(node,xpath)
    except IndexError:          # xpath search found 0 matches
        return None
