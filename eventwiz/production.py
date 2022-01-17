import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# TODO:change DEBUG to false when doing final deployment
DEBUG = False

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'





