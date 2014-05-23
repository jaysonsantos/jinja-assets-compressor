import hashlib
import os

from bs4 import BeautifulSoup
from jinja2 import nodes
from jinja2.ext import Extension

from jac import compile

try:
    from collections import OrderedDict
except ImportError:
    from jac.compat.ordereddict import OrderedDict


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

    def _render_block(self, filename, type):
        """Returns an html element pointing to filename as a string.
        """
        filename = '%s/%s' % (self.environment.compressor_static_prefix, os.path.basename(filename))

        if type.lower() == 'css':
            return '<link type="text/css" rel="stylesheet" href="%s" />' % filename
        elif type.lower() == 'js':
            return '<script type="text/javascript" src="%s"></script>' % filename
        else:
            raise RuntimeError('Unsupported type of compression %s' % type)

    def _find_file(self, path):
        if callable(self.environment.compressor_source_dirs):
            filename = self.environment.compressor_source_dirs(path)
            if os.path.exists(filename):
                return filename
        else:
            if isinstance(self.environment.compressor_source_dirs, basestring):
                dirs = [self.environment.compressor_source_dirs]
            else:
                dirs = self.environment.compressor_source_dirs

            for d in dirs:
                filename = os.path.join(d, path)
                if os.path.exists(filename):
                    return filename

        raise IOError(2, 'File not found %s' % path)

    def _make_hash(self, html, compilables):
        html_hash = hashlib.sha256(html)

        for c in compilables:
            if c.get('src') or c.get('href'):
                with open(self._find_file(str(c.get('src') or c.get('href'))), 'rb') as f:
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
        html = caller()

        enabled = (not hasattr(self.environment, 'compressor_enabled') or
                        self.environment.compressor_enabled is not False)
        if not enabled:
            return html

        debug = (hasattr(self.environment, 'compressor_debug') and
                      self.environment.compressor_debug is True)
        compression_type = compression_type.lower()
        soup = BeautifulSoup(html)
        compilables = self._find_compilable_tags(soup)
        outdir = str(self.environment.compressor_output_dir)
        static_prefix = str(self.environment.compressor_static_prefix)
        assets = OrderedDict()

        html_hash = self._make_hash(html, self._find_compilable_tags(soup))

        if not os.path.exists(str(self.environment.compressor_output_dir)):
            os.makedirs(str(self.environment.compressor_output_dir))

        cached_file = os.path.join(str(self.environment.compressor_output_dir),
                                   '%s.%s') % (html_hash, compression_type)

        if os.path.exists(cached_file):
            return self._render_block(cached_file, compression_type)

        count = 0
        for c in compilables:
            if c.get('type') is None:
                raise RuntimeError('Tags to be compressed must have a compression_type.')

            src = c.get('src') or c.get('href')
            if src:
                filename = os.path.basename(str(src)).split('.', 1)[0]
                uri_cwd = os.path.join(static_prefix, os.path.dirname(str(src)))
                src = open(self._find_file(str(src)), 'rb')
                cwd = os.path.dirname(src.name)
            else:
                uri_cwd = None
                filename = 'inline{0}'.format(count)
                src = c.string
                cwd = None

            needs_compile = c['type'] != 'text/javascript'
            if not debug or needs_compile:
                text = compile(self._get_contents(src), c['type'], cwd=cwd,
                               uri_cwd=uri_cwd, debug=debug)
            else:
                text = self._get_contents(src)

            if not debug:
                outfile = cached_file
            else:
                outfile = os.path.join(outdir, '%s-%s.%s') % (html_hash,
                          filename, compression_type)

            if assets.get(outfile) is None:
                assets[outfile] = ''
            assets[outfile] += text

            count += 1

        blocks = ''
        for outfile, asset in assets.items():
            with open(outfile, 'w') as f:
                f.write(asset)
            blocks += self._render_block(outfile, compression_type)

        return blocks
