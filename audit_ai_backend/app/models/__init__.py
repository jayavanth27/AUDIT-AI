from sqlalchemy.orm import declarative_base

Base = declarative_base()

# import all model modules so they are registered with the metadata
from .user import User  # noqa: F401
from .engagement import Engagement  # noqa: F401
from .document import Document  # noqa: F401
from .extractedfield import ExtractedField  # noqa: F401
from .riskflag import RiskFlag  # noqa: F401
from .workingpaper import WorkingPaper  # noqa: F401
