# based on https://gist.github.com/3912465
# author: bartebrak
#
# A Terminator plugin to open filepaths in PyCharm
#
# Yes, prints are dirty but are useful for debug and development

import os
import terminatorlib.plugin as plugin
import subprocess

import time
from terminatorlib.terminator import Terminator

AVAILABLE = ['OpenInPyCharm']

# finding files is expensive, cache them, might fail you 
# if you change dir structure a lot and happen to cause
# name collision
find_cache = {}

# If I only knew how to enable config via plugins tab
PY_CHARM_BIN = '/usr/local/bin/charm'
# The paths that you will find in terminal might not be complete, 
# Pycharm needs absolute paths unless your project is in the exact same
# folder your paths start with, so I wnat to find the files in a given path
# and get their absolute paths.
HAYSTACK = os.path.expanduser('~') + '/workspace'


class OpenInPyCharm(plugin.URLHandler):
    capabilities = ['url_handler']
    handler_name = 'open_in_py_charm'
    nameopen = "Open in PyCharm"

    # a path:
    #  - starts with a letter or dot
    #  - contains at least one '/'
    #  - consists of letters, number and '_-./'
    match = r'\b[a-zA-Z.]{1}[a-zA-Z0-9_-.]+/[a-zA-Z0-9_-.\/]+\b'

    def callback(self, url):
        print 'matched:', repr(url)
        file_path = self.find(HAYSTACK, url)
        print 'opening:', file_path
        subprocess.call([PY_CHARM_BIN, file_path])
        return "some_random_string_just_so_that_opening_the_resulting_url_will_fail"

    @staticmethod
    def find(start_path, needle):
        if needle in find_cache:
            print 'in cache', needle
            return find_cache[needle]
        start_time = time.time()
        for root, dirs, files in os.walk(start_path):
            abspath = os.path.abspath(root)
            for f in files:
                file_abspath = '%s/%s' % (abspath, f)
                if file_abspath.endswith(needle):
                    print 'lokup elasped', time.time() - start_time
                    find_cache[needle] = file_abspath
                    print 'lookup found', file_abspath
                    return file_abspath
