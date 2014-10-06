[![Build Status](https://travis-ci.org/jaysonsantos/jinja-assets-compressor.png?branch=master)](https://travis-ci.org/jaysonsantos/jinja-assets-compressor)

jinja-assets-compressor
=======================

A Jinja2 extension to compile and/or compress your assets.

# Installing
```
pip install jac
```
For LESS and CSS support, install [less](https://www.npmjs.org/package/less):<br />
`npm install -g less`

For Sass and SCSS support, install [sass](https://rubygems.org/gems/sass):<br />
`gem install sass`

JavaScript minification is built-in using the Python [rJsmin](https://pypi.python.org/pypi/rjsmin) package.

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
jac = JAC(app)
```
And you are done.


## Offline Compression
JAC supports compressing static assets offline, then deploying to a production server. Here is a script to compress your static assets if using Flask:

```
#!/usr/bin/env python

import os
import shutil
import sys

import jinja2
from jac import CompressorExtension
from jac.contrib.flask import get_template_dirs

from my_flask_app import app


def main():

    env = app.jinja_env

    if os.path.exists(env.compressor_output_dir):
        print('Deleting previously compressed files in {output_dir}'
              .format(output_dir=env.compressor_output_dir))
        shutil.rmtree(env.compressor_output_dir)
    else:
        print('No previous compressed files found in {output_dir}'
              .format(output_dir=env.compressor_output_dir))

    template_dirs = ['my_flask_app/'+x for x in get_template_dirs(app)]

    print('Compressing static assets into {output_dir}'
          .format(output_dir=env.compressor_output_dir))
    compressor = env.extensions['jac.extension.CompressorExtension'].compressor
    compressor.offline_compress(env, template_dirs)

    print 'Finished.'
    return 0


if __name__ == '__main__':
    sys.exit(main())
```


# Running Tests
```
virtualenv venv
. venv/bin/activate
pip install -r requirements_tests.txt
make test
```
