import unittest, os
from datetime import timedelta, datetime

from facebookcloudapi.api.dto import (TextObject, ContactObject, MessageObject, InteractiveObject, LocationObject,
                                      TemplateObject)
from facebookcloudapi.api.dto.types import (MessageType, InteractiveType, HeaderType, GranularityType)
from facebookcloudapi.api.dto.inherited import (NameObject, ActionObject, BodyObject, ButtonObject, HeaderObject,
                                                FooterObject, SectionObject, RowObject)
from facebookcloudapi.api.version_v13_0 import API


class TestAnalytics(unittest.TestCase):
    def setUp(self) -> None:
        self.api = API()

    def test_get_analytics(self):
        today = datetime.now()
        days_ago = today - timedelta(days=90)
        response = self.api.get_analytics(account_id=os.getenv('FACEBOOK_CLOUD_TEST_ACCOUNT_ID'), start=days_ago,
                                          end=today)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_conversation_analytics(self):
        today = datetime.now()
        days_ago = today - timedelta(days=200)
        response = self.api.get_conversation_analytics(account_id=os.getenv('FACEBOOK_CLOUD_TEST_ACCOUNT_ID'),
                                                       start=days_ago,
                                                       end=today, granularity=GranularityType.DAILY)
        print(response.json())
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
