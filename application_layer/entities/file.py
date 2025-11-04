Files = {
    'id': {
        'type': {
            'value': 'number',
            'error_code': '1',
        },
    },
    'type': {
        'type': {
            'value': 'string',
            'error_code': '2',
        },
        'required': {
            'value': 'true',
            'error_code': '3',
        },
        'regex': {
            'value': '^(custom|legal|personal|other)$',
            'error_code': '4',
        },
    },
    'buffer': {
        'type': {
            'value': 'string',
            'error_code': '255',
        },
        'max': {
            'value': 255,
            'error_code': '256',
        },
    },
    'path': {
        'type': {
            'value': 'string',
            'error_code': '255',
        },
        'max': {
            'value': 255,
            'error_code': '256',
        },
        'required': {
            'value': 'true',
            'error_code': '5',
        },
    },
    'filename': {
        'type': {
            'value': 'string',
            'error_code': '10',
        },
        'max': {
            'value': 255,
            'error_code': '11',
        },
        'required': {
            'value': 'true',
            'error_code': '12',
        },
    },
    'mime_type': {
        'type': {
            'value': 'string',
            'error_code': '13',
        },
        'max': {
            'value': 100,
            'error_code': '14',
        },
        'required': {
            'value': 'true',
            'error_code': '15',
        },
    },
    'size': {
        'type': {
            'value': 'number',
            'error_code': '16',
        },
        'required': {
            'value': 'true',
            'error_code': '17',
        },
    },
    'organization_id': {
        'type': {
            'value': 'number',
            'error_code': '2000',
        },
    },
    'created_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '6',
        },
    },
    'updated_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '7',
        },
    },
    'created_by': {
        'type': {
            'value': 'number',
            'error_code': '8',
        },
    },
    'updated_by': {
        'type': {
            'value': 'number',
            'error_code': '9',
        },
    },
}
