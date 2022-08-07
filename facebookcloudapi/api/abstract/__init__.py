from __future__ import annotations

import datetime
import json
import os
import time
from typing import List, Iterator

import requests
from requests.structures import CaseInsensitiveDict

from facebookcloudapi import CLOUD_API_BASE_URL, CLOUD_API_LAST_VERSION
from requests import Session, Response

from facebookcloudapi.api.dto import (MessageObject, ContactObject, InteractiveObject, LocationObject, TemplateObject)
from facebookcloudapi.api.dto.text_object import TextObject
from dotenv import load_dotenv

from facebookcloudapi.api.dto.types import GranularityType
from facebookcloudapi.api.dto.types.analytics import ConversationDimensionsTypes

load_dotenv()


class APIAbstract:
    __session: Session = None
    version = CLOUD_API_LAST_VERSION
    api_url = None
    access_token: str = ""
    __current_limits = None

    def __init__(self, access_token: str = os.getenv('FACEBOOK_CLOUD_ACCESS_TOKEN')):
        assert access_token is not None
        self.api_url = f"{CLOUD_API_BASE_URL}/{self.version}"
        self.access_token = access_token

    def __update_current_limits(self, headers: CaseInsensitiveDict[str]):
        if 'X-Business-Use-Case-Usage' in headers:
            self.__current_limits = json.loads(headers.get('X-Business-Use-Case-Usage', "{}"))

    def before_process_response(self, request: requests.Response):
        self.__update_current_limits(request.headers)

    def get_current_limits(self, account_id: str) -> dict:
        if self.__current_limits is None:
            url = f"{self.api_url}/{account_id}"

            with self.session.get(url) as handler:
                self.before_process_response(handler)

        return self.__current_limits

    def get_qrcode_messages(self, phone_id: str) -> Response:
        url = f"https://graph.facebook.com/v14.0/{phone_id}/message_qrdls"
        with self.session.get(url) as handler:
            self.before_process_response(handler)
            return handler

    def get_phone_numbers(self, account_id: str, fields : list = None) -> Iterator[Response]:
        if fields is None:
            fields = ['id', 'account_mode', 'certificate', 'code_verification_status', 'display_phone_number','is_pin_enabled','name_status','new_certificate','new_name_status','quality_score','status', 'quality_rating']
        url = f"https://graph.facebook.com/v14.0/{account_id}/phone_numbers?fields={','.join(fields)}"
        response = self.session.get(url)
        self.before_process_response(response)
        yield response
        cursors = response.json().get('paging', {}).get('cursors', {})

        while 'after' in cursors and len(response.json().get('data', [])):
            response = self.session.get(url, params={
                "after": cursors["after"]
            })
            self.before_process_response(response)
            response_json = response.json()
            if len(response_json.get('data', [])):
                yield response
                cursors = response_json.get('paging', {}).get('cursors', {})
            else:
                break

    def get_phone_status(self, phone_id: str, fields: list = None) -> Response:
        if fields is None:
            fields = ['id', 'account_mode', 'certificate', 'code_verification_status', 'display_phone_number',
                      'is_pin_enabled', 'name_status', 'new_certificate', 'new_name_status', 'quality_score', 'status', 'quality_rating']
        url = f"https://graph.facebook.com/v14.0/{phone_id}?fields={','.join(fields)}"
        with self.session.get(url) as handler:
            self.before_process_response(handler)
            return handler

    def create_qrcode_message(self, phone_id: str, prefilled_message: str, generate_qr_image: str = "SVG"):
        assert generate_qr_image.lower() in ['svg', 'png'], "generate_qr_image must be SVG or PNG"
        params = {
            'prefilled_message': prefilled_message,
            'generate_qr_image': generate_qr_image
        }
        url = f"https://graph.facebook.com/v14.0/{phone_id}/message_qrdls"
        with self.session.post(url, params=params) as handler:
            self.before_process_response(handler)
            return handler

    def delete_qrcode_message(self, phone_id: str, qrcode_id: str):
        url = f"https://graph.facebook.com/v14.0/{phone_id}/message_qrdls/{qrcode_id}"
        with self.session.delete(url) as handler:
            self.before_process_response(handler)
            return handler

    def get_analytics(self, account_id: str, start: datetime.datetime, end: datetime.datetime,
                      granularity: GranularityType = GranularityType.MONTH,
                      phone_numbers: list = None,
                      product_types: list = None, country_codes: list = None) -> requests.Response:
        """
        https://developers.facebook.com/docs/whatsapp/business-management-api/analytics#an-lise
        :param start:
        :param end:
        :param granularity:
        :param phone_numbers:
        :param product_types:
        :param country_codes:
        :return:
        """

        url = f"https://graph.facebook.com/v14.0/{account_id}"
        params = {'start': time.mktime(start.timetuple()), 'end': time.mktime(end.timetuple()),
                  'granularity': granularity,
                  'phone_numbers': phone_numbers, 'product_types': product_types, 'country_codes': country_codes}
        param_str = "analytics"
        for param_key, param_value in params.items():
            if param_value:
                if isinstance(param_value, GranularityType):
                    param_value = param_value.value
                param_str += f".{param_key}({param_value})"

        with self.session.get(
                url=url,
                params={
                    'fields': param_str
                }
        ) as handler:
            self.before_process_response(handler)
            return handler

    def get_conversation_analytics(self, account_id: str, start: datetime.datetime, end: datetime.datetime,
                                   granularity: GranularityType = GranularityType.MONTHLY,
                                   phone_numbers: list = None, metric_types: list = None,
                                   conversation_types: list = None,
                                   conversation_directions: list = None,
                                   dimensions: List[ConversationDimensionsTypes] = [ConversationDimensionsTypes.PHONE,
                                                                                    ConversationDimensionsTypes.COUNTRY,
                                                                                    ConversationDimensionsTypes.CONVERSATION_TYPE,
                                                                                    ConversationDimensionsTypes.CONVERSATION_DIRECTION]):
        # https://developers.facebook.com/docs/whatsapp/business-management-api/analytics#conversation-analytics
        url = f"https://graph.facebook.com/v14.0/{account_id}"
        params = {'start': time.mktime(start.timetuple()), 'end': time.mktime(end.timetuple()),
                  'granularity': granularity,
                  'phone_numbers': phone_numbers, 'metric_types': metric_types,
                  'conversation_types': conversation_types,
                  'conversation_directions': conversation_directions}

        params["dimensions"] = [dimension.value for dimension in dimensions] if len(dimensions) else None
        param_str = "conversation_analytics"
        for param_key, param_value in params.items():
            if param_value:
                if isinstance(param_value, GranularityType):
                    param_value = param_value.value

                param_str += f".{param_key}({param_value})"

        with self.session.get(
                url=url,
                params={
                    'fields': param_str
                }
        ) as handler:
            self.before_process_response(handler)
            return handler

    @property
    def session(self) -> Session:
        if not isinstance(self.__session, Session):
            self.start_session()
            self.__session.headers.update({
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            })

        return self.__session

    def start_session(self):
        self.__session = Session()

    # Message Templates
    def get_message_models(self, account_id: str, after: str = None, before: str = None) -> Response:
        raise NotImplementedError('This function is not implemented in this class or version.'
                                  'Try on a different version.')

    # Send Actions
    def send_message_object(self, from_number_id: str, message_object: MessageObject,
                            object_data: TextObject | ContactObject | InteractiveObject | LocationObject | TemplateObject,
                            messaging_product="whatsapp") -> Response:
        raise NotImplementedError('This function is not implemented in this class or version.'
                                  'Try on a different version.')

    def send_template(self, from_number_id: str, to: str, message_object: MessageObject, object_data: TemplateObject,
                      messaging_product="whatsapp") -> Response:
        raise NotImplementedError('This function is not implemented in this class or version.'
                                  'Try on a different version.')

    def send_message(self, from_number_id: str, message_object: MessageObject, object_data: TextObject,
                     messaging_product="whatsapp") -> Response:
        raise NotImplementedError('This function is not implemented in this class or version.'
                                  'Try on a different version.')

    def send_contact(self, from_number_id: str, message_object: MessageObject, object_data: ContactObject,
                     messaging_product="whatsapp") -> Response:
        raise NotImplementedError('This function is not implemented in this class or version.'
                                  'Try on a different version.')

    def send_interactive(self, from_number_id: str, message_object: MessageObject, object_data: InteractiveObject,
                         messaging_product="whatsapp") -> Response:
        raise NotImplementedError('This function is not implemented in this class or version.'
                                  'Try on a different version.')

    def send_location(self, from_number_id: str, message_object: MessageObject, object_data: LocationObject,
                      messaging_product="whatsapp") -> Response:
        raise NotImplementedError('This function is not implemented in this class or version.'
                                  'Try on a different version.')
