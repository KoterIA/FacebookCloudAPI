import unittest, os

from facebookcloudapi.api.dto import (TextObject, ContactObject, MessageObject, InteractiveObject, LocationObject,
                                      TemplateObject)
from facebookcloudapi.api.dto.types import (MessageType, InteractiveType, HeaderType)
from facebookcloudapi.api.dto.inherited import (NameObject, ActionObject, BodyObject, ButtonObject, HeaderObject,
                                                FooterObject, SectionObject, RowObject)
from facebookcloudapi.api.version_v13_0 import API


class TestMessageModels(unittest.TestCase):
    def setUp(self) -> None:
        self.api = API()

    def test_list_message_models(self):
        for result in self.api.get_message_models(account_id=os.getenv('FACEBOOK_CLOUD_TEST_ACCOUNT_ID')):
            print(result.json())


if __name__ == '__main__':
    unittest.main()
