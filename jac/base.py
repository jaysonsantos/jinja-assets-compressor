# -*- coding: utf-8 -*-

import hashlib
import os

from bs4 import BeautifulSoup

from jac.compat import basestring
from jac.compat import file
from jac.compat import open
from jac.compat import u
from jac.compat import utf8_encode
from jac.config import Config
from jac.exceptions import OfflineGenerationError
from jac.exceptions import TemplateDoesNotExist
from jac.exceptions import TemplateSyntaxError
from jac.parser import Jinja2Parser

try:
    from collections import OrderedDict  # Python >= 2.7
except ImportError:
    from ordereddict import OrderedDict  # Python 2.6

try:
    import lxml  # noqa
    PARSER = 'lxml'
except ImportError:
    PARSER = 'html.parser'


class Compressor(object):

    def __init__(self, **kwargs):
        if 'environment' in kwargs:
            configs = self.get_configs_from_environment(kwargs['environment'])
            self.config = Config(**configs)
        else:
            self.config = Config(**kwargs)

    def compress(self, html, compression_type):

        if not self.config.compressor_enabled:
            return html

        compression_type = compression_type.lower()
        html_hash = self.make_hash(html)

        if not os.path.exists(u(self.config.compressor_output_dir)):
            os.makedirs(u(self.config.compressor_output_dir))

        cached_file = os.path.join(
            u(self.config.compressor_output_dir),
            u('{hash}.{extension}').format(
                hash=html_hash,
                extension=compression_type,
            ),
        )

        if not self.config.compressor_debug and os.path.exists(cached_file):
            filename = os.path.join(
                u(self.config.compressor_static_prefix),
                os.path.basename(cached_file),
            )
            return self.render_element(filename, compression_type)

        assets = OrderedDict()
        soup = BeautifulSoup(html, PARSER)
        for count, c in enumerate(self.find_compilable_tags(soup)):

            url = c.get('src') or c.get('href')
            if url:
                filename = os.path.basename(u(url)).split('.', 1)[0]
                uri_cwd = os.path.join(u(self.config.compressor_static_prefix), os.path.dirname(u(url)))
                text = open(self.find_file(u(url)), 'r', encoding='utf-8')
                cwd = os.path.dirname(text.name)
            else:
                filename = u('inline{0}').format(count)
                uri_cwd = None
                text = c.string
                cwd = None

            mimetype = c['type'].lower()
            try:
                compressor = self.config.compressor_classes[mimetype]
            except KeyError:
                msg = u('Unsupported type of compression {0}').format(mimetype)
                raise RuntimeError(msg)

            if not self.config.compressor_debug:
                outfile = cached_file
            else:
                outfile = os.path.join(
                    u(self.config.compressor_output_dir),
                    u('{hash}-{filename}.{extension}').format(
                        hash=html_hash,
                        filename=filename,
                        extension=compression_type,
                    ),
                )

            if os.path.exists(outfile):
                assets[outfile] = None
                continue

            text = self.get_contents(text)
            compressed = compressor.compile(text,
                                            mimetype=mimetype,
                                            cwd=cwd,
                                            uri_cwd=uri_cwd,
                                            debug=self.config.compressor_debug)

            if not os.path.exists(outfile):
                if assets.get(outfile) is None:
                    assets[outfile] = u('')
                assets[outfile] += u("\n") + compressed

        blocks = u('')
        for outfile, asset in assets.items():
            if not os.path.exists(outfile):
                with open(outfile, 'w', encoding='utf-8') as fh:
                    fh.write(asset)
            filename = os.path.join(
                u(self.config.compressor_static_prefix),
                os.path.basename(outfile),
            )
            blocks += self.render_element(filename, compression_type)

        return blocks

    def make_hash(self, html):
        soup = BeautifulSoup(html, PARSER)
        compilables = self.find_compilable_tags(soup)
        html_hash = hashlib.md5(utf8_encode(html))

        for c in compilables:
            url = c.get('src') or c.get('href')
            if url:
                with open(self.find_file(url), 'r', encoding='utf-8') as f:
                    while True:
                        content = f.read(1024)
                        if content:
                            html_hash.update(utf8_encode(content))
                        else:
                            break

        return html_hash.hexdigest()

    def find_file(self, path):
        if callable(self.config.compressor_source_dirs):
            filename = self.config.compressor_source_dirs(path)
            if os.path.exists(filename):
                return filename
        else:
            if isinstance(self.config.compressor_source_dirs, basestring):
                dirs = [self.config.compressor_source_dirs]
            else:
                dirs = self.config.compressor_source_dirs

            for d in dirs:
                if self.config.compressor_static_prefix_precompress is not None and path.startswith('/'):
                    path = path.replace(self.config.compressor_static_prefix_precompress, '', 1).\
                        lstrip(os.sep).lstrip('/')
                filename = os.path.join(d, path)
                if os.path.exists(filename):
                    return filename

        raise IOError(2, u('File not found {0}').format(path))

    def find_compilable_tags(self, soup):
        tags = ['link', 'style', 'script']
        for tag in soup.find_all(tags):

            # don't compress externally hosted assets
            src = tag.get('src') or tag.get('href')
            if src and (src.startswith('http') or src.startswith('//')):
                continue

            if tag.get('type') is None:
                if tag.name == 'script':
                    tag['type'] = 'text/javascript'
                if tag.name == 'style':
                    tag['type'] = 'text/css'
            else:
                tag['type'] = tag['type'].lower()

            if tag.get('type') is None:
                raise RuntimeError(u('Tags to be compressed must have a type attribute: {0}').format(u(tag)))

            yield tag

    def get_contents(self, src):
        if isinstance(src, file):
            return u(src.read())
        else:
            return u(src)

    def render_element(self, filename, type):
        """Returns an html element pointing to filename as a string.
        """
        if type.lower() == 'css':
            return u('<link type="text/css" rel="stylesheet" href="{0}">').format(filename)
        elif type.lower() == 'js':
            return u('<script type="text/javascript" src="{0}"></script>').format(filename)
        else:
            raise RuntimeError(u('Unsupported type of compression {0}').format(type))

    def get_configs_from_environment(self, environment):
        configs = {}
        for key in dir(environment):
            if key.startswith('compressor_'):
                configs[key] = getattr(environment, key)
        return configs

    def offline_compress(self, environment, template_dirs):

        if isinstance(template_dirs, basestring):
            template_dirs = [template_dirs]

        configs = self.get_configs_from_environment(environment)
        self.config.update(**configs)

        compressor_nodes = {}
        parser = Jinja2Parser(charset='utf-8', env=environment)
        for template_path in self.find_template_files(template_dirs):
            try:
                template = parser.parse(template_path)
            except IOError:  # unreadable file -> ignore
                continue
            except TemplateSyntaxError:  # broken template -> ignore
                continue
            except TemplateDoesNotExist:  # non existent template -> ignore
                continue
            except UnicodeDecodeError:
                continue

            try:
                nodes = list(parser.walk_nodes(template))
            except (TemplateDoesNotExist, TemplateSyntaxError):
                continue
            if nodes:
                template.template_name = template_path
                compressor_nodes.setdefault(template, []).extend(nodes)

        if not compressor_nodes:
            raise OfflineGenerationError(
                "No 'compress' template tags found in templates. "
                "Try setting follow_symlinks to True")

        for template, nodes in compressor_nodes.items():
            for node in nodes:
                parser.render_node({}, node, globals=environment.globals)

    def find_template_files(self, template_dirs):
        templates = set()
        for d in template_dirs:
            for root, dirs, files in os.walk(d, followlinks=self.config.compressor_follow_symlinks):
                templates.update(os.path.join(root, name) for name in files if not name.startswith('.'))
        return templates
