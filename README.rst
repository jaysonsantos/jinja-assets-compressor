.. image:: https://travis-ci.org/jaysonsantos/jinja-assets-compressor.svg?branch=master
    :target: https://travis-ci.org/jaysonsantos/jinja-assets-compressor
    :alt: Build Status

jinja-assets-compressor
=======================

A Jinja2 extension to compile and/or compress your assets.


Installing
----------

::

    pip install jac

For LESS and CSS support, install `less <https://www.npmjs.org/package/less>`_::

    npm install -g less

For COFFEE support, install `coffee-script <https://www.npmjs.com/package/coffee-script>`_::

    npm install -g coffee-script

For Sass and SCSS support, install `sass <https://rubygems.org/gems/sass>`_::

    gem install sass

JavaScript minification is built-in using the Python
`rJsmin <https://pypi.python.org/pypi/rjsmin>`_ package.

When installing on Mac OS X set this shell variable, because jac dependencies
contain C code::

    export CFLAGS=-Qunused-arguments


Usage
-----

To use it, you just have to put your css or js inside a compress tag.

.. code-block:: python

    {% compress 'css' %}
    <style type="text/sass">
    sass stuff
    </style>
    <link rel="stylesheet" type="text/sass" href="file.sass">
    {% endcompress %}

    {% compress 'js' %}
    <script type="text/coffeescript">
    coffee stuff
    </script>
    <script type="text/coffeescript" src="file.coffee"></script>
    {% endcompress %}


Configuring Jinja
-----------------

You just have to create an environment with jac on it and configure output dir,
static prefix and say where it can find your sources.

.. code-block:: python

    import jinja2

    from jac import CompressorExtension

    env = jinja2.Environment(extensions=[CompressorExtension])
    env.compressor_output_dir = './static/dist'
    env.compressor_static_prefix = '/static'
    env.compressor_source_dirs = './static_files'

After that just use ``template = env.from_string(html); template.render()`` to
get it done.


Configuring Flask
-----------------

Where you configure your app, just do this:

.. code-block:: python

    from jac.contrib.flask import JAC

    app = Flask(__name__)
    app.config['COMPRESSOR_DEBUG'] = app.config.get('DEBUG')
    app.config['COMPRESSOR_OUTPUT_DIR'] = './static/dist'
    app.config['COMPRESSOR_STATIC_PREFIX'] = '/static'
    jac = JAC(app)

And you are done.


Offline Compression
-------------------

JAC supports compressing static assets offline, then deploying to a production
server. Here is a command to compress your static assets if using Flask: ::

    python -m jac.contrib.flask my_flask_module:create_app

Replace ``my_flask_module`` with the correct import path to find your Flask app.


Custom Compressors
------------------

The ``compressor_classes`` template env variable tells jac which compressor to
use for each mimetype. The default value for ``compressor_classes`` is:

.. code-block:: python

    {
        'text/css': LessCompressor,
        'text/coffeescript': CoffeeScriptCompressor,
        'text/less': LessCompressor,
        'text/javascript': JavaScriptCompressor,
        'text/sass': SassCompressor,
        'text/scss': SassCompressor,
    }

To use an alternate compressor class, provide a class with a ``compile`` class
method accepting arg ``text`` and kwargs ``mimetype``, ``cwd``, ``uri_cwd``,
and ``debug``. For example, to use
`libsass-python <https://github.com/dahlia/libsass-python>`_ for SASS files
instead of the built-in SassCompressor, create your custom compressor class:

.. code-block:: python

    import sass

    class CustomSassCompressor(object):
        """Custom compressor for text/sass mimetype.

        Uses libsass-python for compression.
        """

        @classmethod
        def compile(cls, text, cwd=None, **kwargs):

            include_paths = []
            if cwd:
                include_paths += [cwd]

            return sass.compile(string=text, include_paths=include_paths)

Then tell jac to use your custom compressor for ``text/sass`` mimetypes:

.. code-block:: python

    env.compressor_classes['text/sass'] = CustomSassCompressor

The equivalent for Flask is:

.. code-block:: python

    jac.set_compressor('text/sass', CustomSassCompressor)

To only customize the path of a compressor which forks a subprocess for the
compile step (LessCompressor, CoffeeScriptCompressor, and SassCompressor), just
extend the compressor class and overwrite the ``binary`` class attribute:

.. code-block:: python

    from jac.compressors import SassCompressor

    class CustomSassCompressor(SassCompressor):
        """Custom SASS compressor using Compass binary instead of libsass for text/sass mimetype.

        Uses the faster libsass wrapper sassc for SASS compression.
        https://github.com/sass/sassc
        """

        binary = '/usr/bin/sassc'

    # Tell Flask to use our custom SASS compressor
    jac.set_compressor('text/sass', CustomSassCompressor)


Running Tests
-------------

::

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements_tests.txt
    make coverage
    make lint

Or use tox to run with multiple python versions:

::

    pip install tox
    tox
