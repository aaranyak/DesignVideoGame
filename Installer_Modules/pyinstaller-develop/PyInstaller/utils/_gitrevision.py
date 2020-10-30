#
# The content of this file will be filled in with meaningful data
# when creating an archive using `git archive` or by downloading an
# archive from github, e.g. from github.com/.../archive/develop.zip
#
rev = "53b67062dd"     # abbreviated commit hash
commit = "53b67062dd456a9a620d46dccbb338af6276bb0a"  # commit hash
date = "2020-10-19 16:42:34 +1100"   # commit date
author = "dcgloe <dcgloe@gmail.com>"
ref_names = "HEAD -> develop"  # incl. current branch
commit_message = """Bootloader: Avoid segfault when temp path is gone (#5255)

If the temp path is removed during application runtime (by a /tmp
cleaning script for example), the application will segfault on exit due
to calling readdir on a NULL pointer. Fix this issue by returning
immediately if the opendir fails.

Co-authored-by: David Gloe <dgloe@cray.com>"""
