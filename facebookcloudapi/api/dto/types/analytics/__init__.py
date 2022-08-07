from enum import Enum


class GranularityType(Enum):
    HALF_HOUR = "HALF_HOUR"
    DAY = "DAY"
    DAILY = 'DAILY'
    MONTH = 'MONTH'
    MONTHLY = 'MONTHLY'

class ConversationDimensionsTypes(Enum):
    PHONE = "phone"
    COUNTRY = "country"
    CONVERSATION_TYPE = "conversation_type"
    CONVERSATION_DIRECTION = "conversation_direction"