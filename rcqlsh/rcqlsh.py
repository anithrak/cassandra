#!/usr/bin/env python3

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import platform
import sys
from glob import glob

import cqlshlib.cqlshmain

if sys.version_info < (3, 6) or sys.version_info >= (3, 12):
    sys.exit("\ncqlsh requires Python 3.6-3.11\n")

# see CASSANDRA-10428
if platform.python_implementation().startswith('Jython'):
    sys.exit("\nCQL Shell does not run on Jython\n")

CQL_LIB_PREFIX = 'cassandra-driver-internal-only-'

CASSANDRA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

print(CASSANDRA_PATH)

# use bundled lib for python-cql if available. if there
# is a ../lib dir, use bundled libs there preferentially.
ZIPLIB_DIRS = [os.path.join(CASSANDRA_PATH, 'lib')]

if platform.system() == 'Linux':
    ZIPLIB_DIRS.append('/usr/share/cassandra/lib')

if os.environ.get('CQLSH_NO_BUNDLED', ''):
    ZIPLIB_DIRS = ()

print(ZIPLIB_DIRS)

def find_zip(libprefix):
    for ziplibdir in ZIPLIB_DIRS:
        zips = glob(os.path.join(ziplibdir, libprefix + '*.zip'))
        if zips:
            return max(zips)   # probably the highest version, if multiple


cql_zip = find_zip(CQL_LIB_PREFIX)
if cql_zip:
    ver = os.path.splitext(os.path.basename(cql_zip))[0][len(CQL_LIB_PREFIX):]
    sys.path.insert(0, os.path.join(cql_zip, 'cassandra-driver-' + ver))

# the driver needs dependencies
third_parties = ('pure_sasl-', 'wcwidth-')

for lib in third_parties:
    lib_zip = find_zip(lib)
    if lib_zip:
        sys.path.insert(0, lib_zip)

try:
    import cassandra
except ImportError as e:
    sys.exit("\nPython Cassandra driver not installed, or not on PYTHONPATH.\n"
             'You might try "pip install cassandra-driver".\n\n'
             'Python: %s\n'
             'Module load path: %r\n\n'
             'Error: %s\n' % (sys.executable, sys.path, e))


# cqlsh should run correctly when run out of a Cassandra source tree,
# out of an unpacked Cassandra tarball, and after a proper package install.
cqlshlibdir = os.path.join(CASSANDRA_PATH, 'pylib')
if os.path.isdir(cqlshlibdir):
    sys.path.insert(0, cqlshlibdir)

CASS_PORT = 9042
CQLPROXY_PORT = 27577
CQLPROXY_ENABLED_FILE = '/var/lib/rubrik/flags/cqlproxy_enabled'

if os.path.isfile(CQLPROXY_ENABLED_FILE):
    DEFAULT_PORT = CQLPROXY_PORT
else:
    DEFAULT_PORT = CASS_PORT
cqlshlib.cqlshmain.DEFAULT_PORT = DEFAULT_PORT

from cqlshlib.cqlshmain import main



# always call this regardless of module name: when a sub-process is spawned
# on Windows then the module name is not __main__, see CASSANDRA-9304 (Windows support was dropped in CASSANDRA-16956)

if __name__ == '__main__':
    sys.argv.append('--protocol-version=4')
    sys.argv.append('--cqlversion=3.4.0')
    print(sys.argv)
    main(sys.argv[1:], CASSANDRA_PATH)