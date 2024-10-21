Users = {
    'id': {
        'type': {'value': "string", 'error_code': "id-type-not-string"}
    },
    'name': {
            'type': { 'value': "string", 'error_code': "name-type-not-string" },
            'no_space': { 'value': 2, 'error_code': 'name-no-space-CUSTOM' },
            'min': { 'value': 1, 'error_code': "name-min-len" },
            'max': { 'value': 128, 'error_code': "name-max-len" },
    },
    'salary': {
        'type': {'value': "number", 'error_code': "salary-type-not-number"},
        'min': {'value': 1000, 'error_code': "salary-too-low"},
        'max': {'value': 1000000, 'error_code': "salary-too-high"},
    }
}
