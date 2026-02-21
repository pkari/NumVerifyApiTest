class ErrorResponses:
    invalid_access_key = {
        'success': False,
        'error': {
            'code': 101,
            'type': 'invalid_access_key',
            'info': 'You have not supplied a valid API Access Key. [Technical Support: support@apilayer.com]'}}

    no_phone_number_provided = {
        'success': False,
        'error': {
            'code': 210,
            'type': 'no_phone_number_provided',
            'info': 'Please specify a phone number. [Example: 14158586273]'}}

    non_numeric_phone_number_provided = {
        'success': False,
        'error': {
            'code': 211,
            'type': 'non_numeric_phone_number_provided',
            'info': 'Please specify a numeric phone number. [Example: 14158586273]'}}
