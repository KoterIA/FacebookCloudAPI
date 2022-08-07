from __future__ import annotations

import os
from typing import List, Iterator
from requests import Session, Response
from facebookcloudapi.api.abstract import APIAbstract
from facebookcloudapi.api.dto.message_object import MessageObject, MessageType
from facebookcloudapi.api.dto import (TextObject, ContactObject, InteractiveObject, LocationObject, TemplateObject)


class API(APIAbstract):
    version = "v13.0"

    def get_message_models(self, account_id: str, limit: int = 3, after: str = None, before: str = None) -> Iterator[
        Response]:
        url = f"{self.api_url}/{account_id}/message_templates"
        params = {'limit': limit, 'after': after, 'before': before}
        params = {k: v for k, v in params.items() if v}
        response = self.session.get(url, params=params)
        self.before_process_response(response)
        yield response
        cursors = response.json().get('paging', {}).get('cursors', {})

        while 'after' in cursors and len(response.json().get('data', [])):
            params['after'] = cursors["after"]
            response = self.session.get(url, params=params)
            self.before_process_response(response)
            response_json = response.json()
            if len(response_json.get('data', [])):
                yield response
                cursors = response_json.get('paging', {}).get('cursors', {})
            else:
                break

    def send_message_object(self, from_number_id: str, message_object: MessageObject,
                            object_data: TextObject | List[
                                ContactObject] | InteractiveObject | LocationObject | TemplateObject,
                            messaging_product="whatsapp") -> Response:
        url = f"{self.api_url}/{from_number_id}/messages"
        object_data_parse = None

        if isinstance(object_data, list):
            object_data_parse = list(map(lambda obj: obj.to_dict(), object_data))
        else:
            object_data_parse = object_data.to_dict()

        data = {
            "type": message_object.message_type.value,
            "messaging_product": messaging_product,
            "to": message_object.to,
            message_object.message_type.value: object_data_parse
        }

        if message_object.recipient_type:
            data["recipient_type"] = message_object.recipient_type

        response = self.session.post(
            url=url,
            json=data
        )
        self.before_process_response(response)
        return response

    def send_message(self, from_number_id: str, message_object: MessageObject, object_data: TextObject,
                     messaging_product="whatsapp") -> Response:
        response = self.send_message_object(
            from_number_id=from_number_id,
            message_object=message_object,
            object_data=object_data,
            messaging_product=messaging_product
        )
        self.before_process_response(response)
        return response

    def send_contact(self, from_number_id: str, message_object: MessageObject, object_data: List[ContactObject],
                     messaging_product="whatsapp") -> Response:
        response = self.send_message_object(
            from_number_id=from_number_id,
            message_object=message_object,
            object_data=object_data,
            messaging_product=messaging_product
        )
        self.before_process_response(response)
        return response

    def send_interactive(self, from_number_id: str, message_object: MessageObject, object_data: InteractiveObject,
                         messaging_product="whatsapp") -> Response:
        response = self.send_message_object(
            from_number_id=from_number_id,
            message_object=message_object,
            object_data=object_data,
            messaging_product=messaging_product
        )
        self.before_process_response(response)
        return response

    def send_location(self, from_number_id: str, message_object: MessageObject, object_data: LocationObject,
                      messaging_product="whatsapp"):
        response = self.send_message_object(
            from_number_id=from_number_id,
            message_object=message_object,
            object_data=object_data,
            messaging_product=messaging_product
        )
        self.before_process_response(response)
        return response

    def send_template(self, from_number_id: str, message_object: MessageObject, object_data: TemplateObject,
                      messaging_product="whatsapp") -> Response:
        response = self.send_message_object(
            from_number_id=from_number_id,
            message_object=message_object,
            object_data=object_data,
            messaging_product=messaging_product
        )
        self.before_process_response(response)
        return response
