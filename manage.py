#!/usr/bin/env python
import os
import sys
if 'INSTALL_COVERAGE' not in os.environ:
    sys.path.insert(0, os.path.abspath('src'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
