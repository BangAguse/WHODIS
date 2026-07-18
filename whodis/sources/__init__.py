"""WHODIS data sources."""

from .validator import check_validator
from .truecaller import check_truecaller
from .getcontact import check_getcontact
from .whatsapp import check_whatsapp
from .telegram import check_telegram
from .instagram import check_instagram
from .facebook import check_facebook
from .linkedin import check_linkedin
from .twitter import check_twitter
from .breach import check_breach
from .virtual import check_virtual
from .spam import check_spam
from .forum import check_forum

__all__ = [
    'check_validator',
    'check_truecaller',
    'check_getcontact',
    'check_whatsapp',
    'check_telegram',
    'check_instagram',
    'check_facebook',
    'check_linkedin',
    'check_twitter',
    'check_breach',
    'check_virtual',
    'check_spam',
    'check_forum',
]

# Map source names to functions
SOURCES_FUNCTIONS = {
    'validator': check_validator,
    'truecaller': check_truecaller,
    'getcontact': check_getcontact,
    'whatsapp': check_whatsapp,
    'telegram': check_telegram,
    'instagram': check_instagram,
    'facebook': check_facebook,
    'linkedin': check_linkedin,
    'twitter': check_twitter,
    'breach': check_breach,
    'virtual': check_virtual,
    'spam': check_spam,
    'forum': check_forum,
}
