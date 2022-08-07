import unittest, os

from facebookcloudapi.api.dto import (TextObject, ContactObject, MessageObject, InteractiveObject, LocationObject,
                                      TemplateObject)
from facebookcloudapi.api.dto.types import (MessageType, InteractiveType, HeaderType)
from facebookcloudapi.api.dto.inherited import (NameObject, ActionObject, BodyObject, ButtonObject, HeaderObject,
                                                FooterObject, SectionObject, RowObject)
from facebookcloudapi.api.version_v13_0 import API


class TestPhoneNumbers(unittest.TestCase):
    def setUp(self) -> None:
        self.api = API()

    def test_get_phonenumbers(self):
        responses = self.api.get_phone_numbers(account_id=os.getenv('FACEBOOK_CLOUD_TEST_ACCOUNT_ID'))

        for response in responses:
            print(response.json())
            self.assertIs(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
