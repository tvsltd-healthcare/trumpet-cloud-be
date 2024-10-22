Organizations = {
    'id': {
        'type': {'value': "string", 'error_code': "id-type-not-string"}
    },
    'name': {
            'type': { 'value': "string", 'error_code': "name-type-not-string" },
            'no_space': { 'value': 2, 'error_code': 'name-no-space-CUSTOM' },
            'min': { 'value': 1, 'error_code': "name-min-len" },
            'max': { 'value': 128, 'error_code': "name-max-len" },
    }
}
