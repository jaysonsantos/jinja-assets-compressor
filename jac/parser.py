from __future__ import absolute_import

import io

import jinja2
import jinja2.ext
from jinja2.nodes import Call
from jinja2.nodes import CallBlock
from jinja2.nodes import ExtensionAttribute

from jac.exceptions import TemplateDoesNotExist
from jac.exceptions import TemplateSyntaxError


class Jinja2Parser(object):
    COMPRESSOR_ID = 'jac.extension.CompressorExtension'

    def __init__(self, charset, env):
        self.charset = charset
        self.env = env

    def parse(self, template_name):
        with io.open(template_name, mode='rb') as file:
            try:
                template = self.env.parse(file.read().decode(self.charset))
            except jinja2.TemplateSyntaxError as e:
                raise TemplateSyntaxError(str(e))
            except jinja2.TemplateNotFound as e:
                raise TemplateDoesNotExist(str(e))

        return template

    def get_nodelist(self, node):
        body = getattr(node, "body", getattr(node, "nodes", []))

        if isinstance(node, jinja2.nodes.If):
            return body + node.else_

        return body

    def _render_nodes(self, context, nodes, globals=None):
        if not isinstance(globals, dict):
            globals = {}
        compiled_node = self.env.compile(jinja2.nodes.Template(nodes))
        template = jinja2.Template.from_code(self.env, compiled_node, globals)
        try:
            rendered = template.render(context)
        except jinja2.exceptions.UndefinedError:
            raise RuntimeError('Only global variables are supported inside compress blocks.')
        return rendered

    def render_nodelist(self, context, node, globals=None):
        return self._render_nodes(context, node.body, globals=globals)

    def render_node(self, context, node, globals=None):
        return self._render_nodes(context, [node], globals=globals)

    def walk_nodes(self, node, block_name=None):
        for node in self.get_nodelist(node):
            if (isinstance(node, CallBlock) and
                isinstance(node.call, Call) and
                isinstance(node.call.node, ExtensionAttribute) and
                    node.call.node.identifier == self.COMPRESSOR_ID):
                node.call.node.name = '_compress_block'
                yield node
            else:
                for node in self.walk_nodes(node, block_name=block_name):
                    yield node
