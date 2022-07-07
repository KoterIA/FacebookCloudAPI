import unittest, os

from facebookcloudapi.api.dto.message_object import MessageObject, MessageType
from facebookcloudapi.api.dto.text_object import TextObject
from facebookcloudapi.api.version_v13_0 import API
from dotenv import load_dotenv


class TestSendMessage(unittest.TestCase):

    def test_send_text(self):
        api = API()
        response = api.send_message(
            from_number_id=os.getenv('FACEBOOK_CLOUD_TEST_NUMBER_ID'),
            message_object=MessageObject(
                message_type=MessageType.TEXT,
                to="5527999425964"
            ),
            object_data=TextObject(
                body="Teste do Henrique"
            )
        )
        self.assertIs(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
