Studies = {
    'id': {
        'type': {
            'value': 'number',
            'error_code': '80',
        },
    },
    'name': {
        'type': {
            'value': 'string',
            'error_code': '81',
        },
        'required': {
            'value': True,
            'error_code': '82',
        },
        'max': {
            'value': 25,
            'error_code': '83',
        },
    },
    'description': {
        'type': {
            'value': 'text',
            'error_code': '84',
        },
    },
    'status': {
        'type': {
            'value': 'string',
            'error_code': '85',
        },
        'regex': {
            'value': '^(active|paused|completed)$',
            'error_code': '86',
        },
        'required': {
            'value': True,
            'error_code': '87',
        },
    },
    'result': {
        'type': {
            'value': 'text',
            'error_code': '88',
        },
        'required': {
            'value': True,
            'error_code': '89',
        },
    },
    'purpose': {
        'type': {
            'value': 'text',
            'error_code': '90',
        },
        'required': {
            'value': True,
            'error_code': '91',
        },
    },
    'created_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '92',
        },
    },
    'updated_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '93',
        },
    },
    'created_by': {
        'type': {
            'value': 'number',
            'error_code': '94',
        },
    },
    'updated_by': {
        'type': {
            'value': 'number',
            'error_code': '95',
        },
    },
}
