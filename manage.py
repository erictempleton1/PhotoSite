#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
<<<<<<< HEAD
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photosite.settings")
=======
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
>>>>>>> 36e6548dd08acbf9146580732a9849fb8d8dc1ec

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
