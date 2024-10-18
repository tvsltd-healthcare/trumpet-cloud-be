Organizations = {
    'id': {
        'type': {'value': "string", 'error_code': "id-type-not-string"}
    },
    'name': {
            'type': { 'value': "string", 'error_code': "name-type-not-string" },
            'no_space': { 'value': 2, 'error_code': 'name-no-space-CUSTOM' },
            'min': { 'value': 1, 'error_code': "name-min-len" },
            'max': { 'value': 128, 'error_code': "name-max-len" },
    },
    # "email": {
    #         'type': { 'value': "string", 'error_code': "email-type-not-string" },
    #         'pattern': { 'value': '^[A-Za-z0-9._%-]@[A-Za-z0-9.-]\\.[A-Za-z]{2,}$', 'error_code': "email-type-not-email"},
    #         'minLength': { 'value': 1, 'error_code': "email-min-len" },
    #         'maxLength': { 'value': 128, 'error_code': "email-max-len" },
    #     }
}
