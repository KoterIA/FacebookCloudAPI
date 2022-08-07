import unittest, os

from facebookcloudapi.api.dto import (TextObject, ContactObject, MessageObject, InteractiveObject, LocationObject,
                                      TemplateObject)
from facebookcloudapi.api.dto.types import (MessageType, InteractiveType, HeaderType)
from facebookcloudapi.api.dto.inherited import (NameObject, ActionObject, BodyObject, ButtonObject, HeaderObject,
                                                FooterObject, SectionObject, RowObject)
from facebookcloudapi.api.version_v13_0 import API


class TestRatingLimits(unittest.TestCase):
    def setUp(self) -> None:
        self.api = API()

    def test_get_limits(self):
        limits = self.api.get_current_limits(account_id=os.getenv('FACEBOOK_CLOUD_TEST_ACCOUNT_ID'))
        self.assertTrue(len(limits.keys()))
        for key, value in limits.items():
            self.assertIs(value, list)


if __name__ == '__main__':
    unittest.main()
