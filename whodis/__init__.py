"""WHODIS — Full OSINT Phone Number Investigator."""

from whodis.utils import VERSION

__version__ = VERSION
__author__ = "Security Researcher"
__description__ = "Full OSINT Phone Number Investigator"

if __name__ == "__main__":
    from whodis.main import main
    main()
