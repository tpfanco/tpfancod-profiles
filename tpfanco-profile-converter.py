#! /usr/bin/python2.7
# -*- coding: utf8 -*-
#
# tpfanco-profile-converter - converts old tpfand profiles to tpfanco
# Copyright (C) 2016 Vladyslav Shtabovenko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import argparse
import collections
from os.path import basename
import sys

from tpfancod import settings
if not ('/usr/lib/python2.7/site-packages' in sys.path):
    sys.path.append('/usr/lib/python2.7/site-packages')


def read_config(path):
    """Reads a fan profile file"""
    trigger_points = {}
    sensor_names = {}
    hysteresis = None
    profile_comment = None
    file = open(path, 'r')
    for line in file.readlines():
        line = line.split('#')[0].strip()
        if len(line) > 0:
            try:
                if (line.count('.') and line.count('=') and line.find('.') < line.find('=')) or (line.count('.') and not line.count('=')):
                    id, rest = line.split('.', 1)
                    id = id.strip()
                    id = int(id)

                    if rest.count('='):
                        name, triggers = rest.split('=', 1)
                        name = name.strip()
                        points = {}
                        for trigger in triggers.strip().split(' '):
                            trigger = trigger.strip()
                            if len(trigger) > 0:
                                temp, level = trigger.split(':')
                                temp = int(temp)
                                points[temp] = int(level)
                        if len(points) > 0:
                            trigger_points[str(id)] = points
                    else:
                        name = rest.strip()
                        triggers = None
                    if len(name) > 0:
                        sensor_names[str(id)] = name

                elif line.count('='):
                    option, value = line.split('=', 1)
                    option = option.strip()
                    value = value.strip()
                    if option == 'hysteresis':
                        hysteresis = int(value)
                    elif option == 'comment':
                        profile_comment = value.replace("\\n", "\n")
                        # verify that comment is valid unicode, otherwise use
                        # Latin1 coding
                        try:
                            unicode(profile_comment)
                        except UnicodeDecodeError:
                            profile_comment = profile_comment.decode(
                                "latin1")
            except Exception, e:
                print "Error parsing line: %s" % line
                print e
    file.close()
    return (trigger_points, sensor_names, hysteresis, profile_comment)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i', '--input', help='location of the profile that needs to be converted', required=True)
    parser.add_argument(
        '-o', '--output', help='path to save the new profile', default='')

    args = parser.parse_args()

    input = args.input
    output = args.output
    profile_name = basename(input)

    act_settings = settings.Settings('Dummy', '/Settings', True, False, True, '',
                                     '', '', '', '', '', '', '')

    (act_settings.trigger_points, act_settings.sensor_names, act_settings.hysteresis,
     act_settings.profile_comment) = read_config(input)

    if profile_name.startswith('lenovo_') or profile_name.startswith('ibm_'):
        (act_settings.product_pretty_vendor,
         act_settings.product_pretty_id) = profile_name.upper().split('_')
    act_settings.product_pretty_name = 'ThinkPad ???'

    act_settings.write_profile(output + profile_name)

if __name__ == '__main__':
    main()
