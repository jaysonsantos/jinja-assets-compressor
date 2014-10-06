[![Build Status](https://travis-ci.org/jaysonsantos/jinja-assets-compressor.png?branch=master)](https://travis-ci.org/jaysonsantos/jinja-assets-compressor)

jinja-assets-compressor
=======================

A Jinja2 extension to compile and/or compress your assets.

# Installing
```
pip install jac
```
For LESS support, install [less](https://www.npmjs.org/package/less):<br />
`npm install -g less`

For Sass and SCSS support, install [sass](https://rubygems.org/gems/sass):<br />
`gem install sass`

JavaScript minification is built-in using the Python [rJsmin](https://pypi.python.org/pypi/rjsmin) package.

CSS minification is built-in using the Python [csscompressor](https://pypi.python.org/pypi/csscompressor) package.

When installing on Mac OS X set this shell variable, because jac dependencies contain C code:<br />
`export CFLAGS=-Qunused-arguments`

# Usage
To use it, you just have to put your css or js inside a compress tag.
```html
{% compress 'css' %}
<style type="text/sass">
sass stuff
</style>
{% endcompress %}

{% compress 'js' %}
<script type="text/coffeescript">
coffee stuff
</script>
<script type="text/coffescript" src="file.coffee"></script>
{% endcompress %}
```

## Configuring Jinja
You just have to create an environment with jac on it and configure output dir, static prefix and say where it can find your sources.

```python
import jinja2

from jac import CompressorExtension

env = jinja2.Environment(extensions=[CompressorExtension])
env.compressor_output_dir = './static/dist'
env.compressor_static_prefix = '/static'
env.compressor_source_dirs = './static_files'
```
After that just use `template = env.from_string(html); template.render()` to get it done.

## Configuring Flask
Where you configure your app, just do this:
```python
from jac.contrib.flask import JAC

app = Flask(__name__)
app.config['COMPRESSOR_DEBUG'] = app.config.get('DEBUG')
app.config['COMPRESSOR_OUTPUT_DIR'] = './static/dist'
app.config['COMPRESSOR_STATIC_PREFIX'] = '/static'
app.config['COMPRESSOR_OFFLINE_COMPRESS'] = not app.config.get('DEBUG')
jac = JAC(app)
```
And you are done.

# Running Tests
```virtualenv venv
. venv/bin/activate
pip install -r requirements_tests.txt
make test
```
