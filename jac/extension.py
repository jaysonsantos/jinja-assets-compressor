import hashlib
import os

from bs4 import BeautifulSoup
from jinja2 import nodes
from jinja2.ext import Extension

from jac import compile


class CompilerExtension(Extension):
    tags = set(['compress'])

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endcompress'], drop_needle=True)

        if len(body) > 1:
            raise RuntimeError('One tag supported for now.')

        return nodes.CallBlock(self.call_method('_compile', args), [], [], body).set_lineno(lineno)

    def _find_compilable_tags(self, soup):
        for link in soup.find_all('link'):
            yield link

        for style in soup.find_all('style'):
            yield style

        for script in soup.find_all('script'):
            yield script

    def _render_block(self, filename, type):
        print filename
        filename = '%s/%s' % (self.environment.compressor_static_prefix, os.path.basename(filename))

        if type.lower() == 'css':
            return '<link type="text/css" rel="stylesheet" src="%s" />' % filename
        elif type.lower() == 'js':
            return '<script type="text/javascript" src="%s"></script>' % filename
        else:
            raise RuntimeError('Unsupported type of compression %s' % type)

    def _find_file(self, path):
        for d in self.environment.compressor_source_dir:
            filename = os.path.join(d, path)
            if os.path.exists(filename):
                return filename

        raise IOError(2, 'File not found %s' % path)

    def _make_hash(self, html, compilables):
        html_hash = hashlib.sha256(html)

        for c in compilables:
            if c.get('src'):
                with open(self._find_file(c['src']), 'rb') as f:
                    while True:
                        content = f.read(1024)
                        if content:
                            html_hash.update(content)
                        else:
                            break

        return html_hash.hexdigest()

    def _get_contents(self, src):
        if isinstance(src, file):
            return src.read()
        else:
            return src

    def _compile(self, compression_type, caller):
        compression_type = compression_type.lower()
        html = caller()
        soup = BeautifulSoup(html)
        compilables = self._find_compilable_tags(soup)
        text = ''

        html_hash = self._make_hash(html, self._find_compilable_tags(soup))

        cached_file = os.path.join(str(self.environment.compressor_output_dir),
                                   '%s.%s') % (html_hash, compression_type)

        if os.path.exists(cached_file):
            return self._render_block(cached_file, compression_type)

        for c in compilables:
            if c.get('type') is None:
                raise RuntimeError('Tags to be compressed must have a compression_type.')

            src = c.get('src')
            if src:
                src = open(self._find_file(src), 'rb')
            else:
                src = c.string

            if c.name == 'link' and c.get('rel', [''])[0].lower() != 'stylesheet':
                text += self._get_contents(src)

            if c['type'].lower() in ('text/css', 'text/javascript'):
                text += self._get_contents(src)
            else:
                text += compile(self._get_contents(src), c['type'])

        with open(cached_file, 'w') as f:
            f.write(text)

        return self._render_block(cached_file, compression_type)
