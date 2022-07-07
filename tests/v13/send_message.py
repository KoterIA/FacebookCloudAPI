import unittest, os

from facebookcloudapi.api.dto import (TextObject, ContactObject, MessageObject)
from facebookcloudapi.api.dto.types import (MessageType, ContactType)
from facebookcloudapi.api.dto.inherited import NameObject
from facebookcloudapi.api.version_v13_0 import API


class TestSendMessage(unittest.TestCase):
    def setUp(self) -> None:
        self.api = API()

    def test_send_text(self):
        response = self.api.send_message(
            from_number_id=os.getenv('FACEBOOK_CLOUD_TEST_NUMBER_ID'),
            message_object=MessageObject(
                message_type=MessageType.TEXT,
                to=os.getenv('FACEBOOK_CLOUD_TEST_TO')
            ),
            object_data=TextObject(
                body="Hello World!"
            )
        )
        self.assertIs(response.status_code, 200)
        response.close()

    def test_send_contact(self):
        response = self.api.send_contact(
            from_number_id=os.getenv('FACEBOOK_CLOUD_TEST_NUMBER_ID'),
            message_object=MessageObject(
                message_type=MessageType.CONTACTS,
                to=os.getenv('FACEBOOK_CLOUD_TEST_TO')
            ),
            object_data=[ContactObject(
                name=NameObject(
                    formatted_name="Test User",
                    first_name="Test",
                    last_name="User"
                )
            )]
        )
        self.assertIs(response.status_code, 200)
        response.close()


if __name__ == '__main__':
    unittest.main()
