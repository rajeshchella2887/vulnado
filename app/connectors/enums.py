from enum import Enum

from django.utils.translation import gettext_lazy as _


class ServiceNowStateEnum(Enum):
    NEW = 1, _("New")
    PROGRESS = 2, _("In-progress")
    ONHOLD = 3, _("On-hold")
    RESOLVED = 6, _("Resolved")
    CLOSED = 7, _("Closed")
    CANCELLED = 8, _("Cancelled")


class ProblemMgtStateEnum(Enum):
    NEW = 101, _("New")
    ASSESS = 102, _("Assess")
    ROOT_CAUSE_ANALYSIS = 103, _("Root Cause Analysis")
    FIX_IN_PROGRESS = 104, _("Fix in Progress")
    RESOLVED = 106, _("Resolved")
    CLOSED = 107, _("Closed")


class ChangeRequestStateEnum(Enum):
    NEW = -5, _("New")
    ASSESS = -4, _("Assess")
    AUTHORIZE = -3, _("Authorize")
    SCHEDULED = -2, _("Scheduled")
    IMPLEMENT = -1, _("Implement")
    REVIEW = 0, _("Review")
    CLOSED = 3, _("Closed")
    CANCELED = 4, _("Canceled")


class SlaStateEnum(Enum):
    YES = "Yes"
    NO = "No"


class PriorityGroupsEnum(Enum):
    CRITICAL = 1, _("Critical")
    HIGH = 2, _("High")
    MODERATE = 3, _("Moderate")
    LOW = 4, _("Low")
    PLANNING = 5, _("Planning")


class MonthlyEnum(Enum):
    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"
    JULY = "July"
    AUGUST = "August"
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"
