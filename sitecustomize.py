"""Repository-wide warning filters."""

import warnings

# Silence noisy pkg_resources deprecation emitted by the fs package during pytest
warnings.filterwarnings("ignore", category=UserWarning, module=r"fs")
