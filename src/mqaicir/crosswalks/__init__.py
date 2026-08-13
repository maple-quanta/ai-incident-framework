"""Conservative external-framework crosswalk suggestions.

Mappings are informative relationships, never equivalence or compliance claims.
"""

from mqaicir.crosswalks.atlas import suggest as suggest_atlas
from mqaicir.crosswalks.nist import suggest as suggest_nist
from mqaicir.crosswalks.oecd import suggest as suggest_oecd
from mqaicir.crosswalks.safe import suggest as suggest_safe

__all__ = ["suggest_atlas", "suggest_nist", "suggest_oecd", "suggest_safe"]

