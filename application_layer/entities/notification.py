Notifications = {
    'id': {
        'type': {
            'value': 'number',
            'error_code': '1502',
        },
    },
    'user_id': {
        'type': {
            'value': 'number',
            'error_code': '1503',
        },
    },
    'message': {
        'type': {
            'value': 'text',
            'error_code': '1504',
        },
        'required': {
            'value': True,
            'error_code': '1505',
        },
    },
    'is_read': {
    },
    'type': {
        'regex': {
            'value': '^(organization_approved|user_approved)$',
            'error_code': '1506',
        },
    },
    'read_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '1507',
        },
    },
    'created_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '1508',
        },
    },
    'updated_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '1509',
        },
    },
    'created_by': {
        'type': {
            'value': 'number',
            'error_code': '1510',
        },
    },
    'updated_by': {
        'type': {
            'value': 'number',
            'error_code': '1511',
        },
    },
}
