import os
import pytest

from constants.error_responses import ErrorResponses
from constants.http_responses import HTTPResponse
from helpers.assert_error_response import assert_error_response
from helpers.schema_validator import JSONHelper
from api.numverify_api import NumVerifyAPI
from assertpy import assert_that, soft_assertions

from tests.base_test import BaseTest


class TestNumVerifyAPI(BaseTest):

    @classmethod
    def setup_class(cls):

        api_key = os.getenv("NUMVERIFY_API_KEY")
        if not api_key:
            raise ValueError("NUMVERIFY_API_KEY environment variable not set")
        cls.api = NumVerifyAPI(api_key)
        cls.logger.info("NumVerifyAPI initialized with provided API key.")

    @pytest.mark.jira('JIRA-1234')
    @pytest.mark.testrail('TR-5678')
    @pytest.mark.parametrize("number, country_code, j_format", [
            pytest.param(14158586273, "", "", id="Valid default values"),
            pytest.param(201234567, 'HU', 1, id="Valid HU number")
        ])
    def test_number_verified(self, number, country_code, j_format, request):
        self.log_test_metadata(request)
        self.logger.info(f"Testing number verification: number={number}, country_code={country_code}, j_format={j_format}")
        response = self.api.get_number_validation(number, country_code, j_format)
        self.logger.info(f"Received response: status_code={response.status_code}, body={response.text}")
        assert response.status_code == HTTPResponse.OK
        data = response.json()
        with soft_assertions():
            assert_that(JSONHelper.schema_validator(data, "GET_numverify.json"), "Response JSON does not match schema").is_true()
            assert_that(data['valid'], f"Response validity is not correct. Expected: {True}, "
                                       f"but got: {data['valid']}").is_true()
            assert_that(data['number'], f"Response number is not correct. Expected: {number}, "
                                        f"but got: {data['number']}").contains(str(number))
            assert_that(['US', country_code], f"Response country code is not correct. Expected: {country_code}, "
                                              f"but got: {data['country_code']}").contains(data['country_code'])

    @pytest.mark.jira('JIRA-1234')
    @pytest.mark.testrail('TR-5679')
    @pytest.mark.parametrize("api_key, number, expected_status, expected_error", [
        pytest.param(None, None, HTTPResponse.BAD_REQUEST, ErrorResponses.no_phone_number_provided,
                     id="no_phone_number"),
        pytest.param("INVALID_KEY", "14158586273", HTTPResponse.OK, ErrorResponses.invalid_access_key,
                     id="invalid_access_key"),
        pytest.param(None, "!@#$%", HTTPResponse.BAD_REQUEST, ErrorResponses.non_numeric_phone_number_provided,
                     id="Special characters"),
        pytest.param(None, "", HTTPResponse.BAD_REQUEST, ErrorResponses.no_phone_number_provided,
                     id="Empty string phone number"),
    ])
    def test_error_responses(self, api_key, number, expected_status, expected_error, request):
        self.log_test_metadata(request)
        self.logger.info(f"Testing error response: api_key={api_key}, number={number}")
        api = self.api if api_key is None else NumVerifyAPI(api_key)
        response = api.get_number_validation(number)
        self.logger.info(f"Received response: status_code={response.status_code}, body={response.text}")
        assert response.status_code == expected_status
        data = response.json()
        assert_error_response(data, expected_error)

    @pytest.mark.jira('JIRA-1234')
    @pytest.mark.testrail('TR-5680')
    @pytest.mark.parametrize("number, country_code, j_format, expected_status, expected_valid", [
        pytest.param("abc123", "", 1, HTTPResponse.OK, False, id="Non-numeric input"),
        pytest.param(1234567, "US", 1, HTTPResponse.OK, True, id="Shortest valid US number"),
        pytest.param(123456789012345, "US", 1, HTTPResponse.OK, False, id="Longest valid US number"),
        pytest.param(14158586273, "ZZ", 1, HTTPResponse.OK, True, id="Invalid country code"),
        pytest.param(14158586273, "US", -1, HTTPResponse.OK, True, id="Invalid format"),
    ])
    def test_number_validation_edge_cases(self, number, country_code, j_format, expected_status, expected_valid,
                                          request):
        self.log_test_metadata(request)
        self.logger.info(f"Testing edge case: number={number}, country_code={country_code}, j_format={j_format}")
        response = self.api.get_number_validation(number, country_code, j_format)
        self.logger.info(f"Received response: status_code={response.status_code}, body={response.text}")
        assert response.status_code == expected_status
        data = response.json()
        assert_that(data['valid']).is_equal_to(expected_valid)
