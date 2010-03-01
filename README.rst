GoCaptain start and stop scripts
================================

The GoCaptain [#]_ buildout recipe produces a script to start and stop daemons,
similar to those you find in /etc/init.d.  By default it will inspect your
system and either write a "simple" script, such as you might produce yourself
or produce a LinuxStandard Base variation, that provides more tooling.

In particular the LSB scripts will try multiple times to shut down your daemon,
and will not start it if it is already running.

This package also provides a simple way to produce these scripts from other
buildout recipes - see `isotoma.recipe.varnish`_ for an example.

.. _`isotoma.recipe.varnish`: http://pypi.python.org/pypi/isotoma.recipe.varnish

The buildout recipe
-------------------

A simple example would be::

    [example]
    recipe = isotoma.recipe.gocaptain
    daemon = /usr/bin/example
    name = example
    description = example daemon for that thing i did that time
    pidfile = /var/tmp/example.pid
    args = 
        -P ${example:pidfile}
        -w /var/tmp/example.log

This will produce a script in bin/example that launches your daemon, and shuts
it down again later, using the PID in the pidfile.

Options
~~~~~~~

The mandatory options this recipe accepts are:

daemon
    The path to the daemon executable file
name
    The name of the daemon, displayed in log messages
description
    A longer description, shown on the console during start and stop
pidfile
    A path to a file to store the PID of the new daemon in
args
    The arguments for the daemon.  These will be formatted in the output script as you provide them, with continuations provided as needed

In addition you can provide:

template
    A path to the template for your start/stop script.  This will be used in preference to the templates provided with this package.

Calling from other code
-----------------------

If you wish to use this from one of your own recipes, I suggest you do
something like::

    from isotoma.recipe import gocaptain
    gc = gocaptain.Automatic()
    f = open("/path/to/script", "w")
    gc.write(f, daemon="/usr/sbin/thing", 
             args="-D -P /path/to/pid",
             name="my thing", description="thing")
    f.close()
    os.chmod(target, 0755)

The Automatic module will select the Simple or LinuxStandardBase variants, by
inspecting your system (very simplisticly!).

License
-------

Copyright 2010 Isotoma Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

.. [#] The name comes from Cordwainer Smith

