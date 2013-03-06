[![Build Status](https://travis-ci.org/jaysonsantos/jinja-assets-compressor.png?branch=master)](https://travis-ci.org/jaysonsantos/jinja-assets-compressor)

jinja-assets-compressor
=======================

A Jinja2 extension to compile and/or compress your assets.

# Installing
```
pip install jac
```

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

from jac import CompilerExtension

env = jinja2.Environment(extensions=[CompilerExtension])
env.compressor_output_dir = tmpdir
env.compressor_static_prefix = '/static'
env.compressor_source_dirs = './static_files'
```
After that just use `template = env.from_string(html); template.render()` to get it done.

## Configuring Flask
Where you configure your app, just do this:
```python
from jac.contrib.flask import JAC

app = Flask(__name__)
jac = JAC(app)
```
And you are done.
