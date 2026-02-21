from assertpy import assert_that, soft_assertions


def assert_error_response(data, expected):
    with soft_assertions():
        assert_that(data['success']).is_equal_to(expected['success'])
        assert_that(data['error']['code'], "error code mismatch.").is_equal_to(expected['error']['code'])
        assert_that(data['error']['type'], "error type mismatch.").is_equal_to(expected['error']['type'])
        assert_that(data['error']['info'], "error info mismatch.").is_equal_to(expected['error']['info'])
