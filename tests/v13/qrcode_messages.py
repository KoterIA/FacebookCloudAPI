import unittest, os

from facebookcloudapi.api.dto import (TextObject, ContactObject, MessageObject, InteractiveObject, LocationObject,
                                      TemplateObject)
from facebookcloudapi.api.dto.types import (MessageType, InteractiveType, HeaderType)
from facebookcloudapi.api.dto.inherited import (NameObject, ActionObject, BodyObject, ButtonObject, HeaderObject,
                                                FooterObject, SectionObject, RowObject)
from facebookcloudapi.api.version_v13_0 import API


class TestQRCodeMessagest(unittest.TestCase):
    def setUp(self) -> None:
        self.api = API()

    def test_get_qrcode_messages(self):
        response = self.api.get_qrcode_messages(phone_id=os.getenv('FACEBOOK_CLOUD_TEST_NUMBER_ID'))
        print(response.json())
        self.assertTrue(response.status_code == 200)

    def test_create_and_delete_qrcode_message(self):
        response = self.api.create_qrcode_message(phone_id=os.getenv('FACEBOOK_CLOUD_TEST_NUMBER_ID'),
                                                  prefilled_message="This is a test!")
        data = response.json()
        print(data)
        self.assertTrue(response.status_code == 200)
        qrcode_id = data.get("code", "")
        response = self.api.delete_qrcode_message(phone_id=os.getenv('FACEBOOK_CLOUD_TEST_NUMBER_ID'), qrcode_id=qrcode_id)
        self.assertTrue(response.status_code == 200)
        print(response.json())


if __name__ == '__main__':
    unittest.main()
