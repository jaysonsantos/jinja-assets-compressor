from bs4 import BeautifulSoup
from jinja2 import nodes
from jinja2.ext import Extension

from jac import compile


class CompilerExtension(Extension):
    tags = set(['compress'])

    def parse(self, parser):
        parser.stream.next()
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endcompress'], drop_needle=True)

        if len(body) > 1:
            raise RuntimeError('One tag supported for now.')

        return nodes.CallBlock(self.call_method('_compile', args), [], [], body)

    def _find_compilable_tags(self, soup):
        for link in soup.find_all('link'):
            yield link

        for style in soup.find_all('style'):
            yield style

        for script in soup.find_all('script'):
            yield script

    def _compile(self, type, caller):
        html = caller()
        soup = BeautifulSoup(html)
        compilables = self._find_compilable_tags(soup)
        text = ''

        for c in compilables:
            if c.get('type') is None:
                raise RuntimeError('Tags to be compressed must have a type.')

            if c.name == 'link' and c.get('rel', [''])[0].lower() != 'stylesheet':
                text += c.string

            if c['type'].lower() in ('text/css', 'text/javascript'):
                text += c.string
            else:
                text += compile(c.string, c['type'])

        if type.lower() == 'css':
            return '<style type="text/css">%s</style>' % text
        elif type.lower() == 'javascript':
            return '<script type="text/javascript">%s</script>' % text
        else:
            raise RuntimeError('Unsupported type of compression %s' % type)
