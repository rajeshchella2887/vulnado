from _datetime import datetime
from connectors import enums
from django import template

register = template.Library()


@register.filter(expects_localtime=True)
@register.tag(name="date_format")
def date_format(value):
    dt_obj_value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    dt_str_value = datetime.strftime(dt_obj_value, "%d-%m-%Y")
    return dt_str_value


@register.filter()
@register.tag(name="state_format")
def state_format(value):
    if value == enums.ServiceNowStateEnum.NEW.value[0]:
        return enums.ServiceNowStateEnum.NEW.value[1]
    elif value == enums.ServiceNowStateEnum.PROGRESS.value[0]:
        return enums.ServiceNowStateEnum.PROGRESS.value[1]
    elif value == enums.ServiceNowStateEnum.ONHOLD.value[0]:
        return enums.ServiceNowStateEnum.ONHOLD.value[1]
    elif value == enums.ServiceNowStateEnum.RESOLVED.value[0]:
        return enums.ServiceNowStateEnum.RESOLVED.value[1]
    elif value == enums.ServiceNowStateEnum.CLOSED.value[0]:
        return enums.ServiceNowStateEnum.CLOSED.value[1]
    elif value == enums.ServiceNowStateEnum.CANCELLED.value[0]:
        return enums.ServiceNowStateEnum.CANCELLED.value[1]


@register.filter()
@register.tag(name="priority_format")
def priority_format(value):
    if value == enums.PriorityGroupsEnum.CRITICAL.value[0]:
        return enums.PriorityGroupsEnum.CRITICAL.value[1]
    elif value == enums.PriorityGroupsEnum.HIGH.value[0]:
        return enums.PriorityGroupsEnum.HIGH.value[1]
    elif value == enums.PriorityGroupsEnum.MODERATE.value[0]:
        return enums.PriorityGroupsEnum.MODERATE.value[1]
    elif value == enums.PriorityGroupsEnum.LOW.value[0]:
        return enums.PriorityGroupsEnum.LOW.value[1]
    elif value == enums.PriorityGroupsEnum.PLANNING.value[0]:
        return enums.PriorityGroupsEnum.PLANNING.value[1]
