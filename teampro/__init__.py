# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = '0.0.1'

# Apply WeasyPrint annexure patch at app load time
try:
    from teampro.patches.patch_weasyprint_annexure import apply_patch
    apply_patch()
except Exception:
    pass
