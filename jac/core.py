# -*- coding: utf-8 -*-


def render_element(filename, type):
    """Returns an html element pointing to filename as a string.
    """
    if type.lower() == 'css':
        return u('<link type="text/css" rel="stylesheet" href="{0}" />').format(filename)
    elif type.lower() == 'js':
        return u('<script type="text/javascript" src="{0}"></script>').format(filename)
    else:
        raise RuntimeError('Unsupported type of compression %s' % type)

def _find_compilable_tags(self, soup):
    tags = ['link', 'style', 'script']
    for tag in soup.find_all(tags):
        if tag.get('type') is None:
            if tag.name == 'script':
                tag['type'] = 'text/javascript'
            if tag.name == 'style':
                tag['type'] = 'text/css'
        else:
            tag['type'] == tag['type'].lower()
        yield tag
