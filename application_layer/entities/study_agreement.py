StudyAgreements = {
    'id': {
        'type': {
            'value': 'number',
            'error_code': '117',
        },
    },
    'purpose': {
        'type': {
            'value': 'string',
            'error_code': '118',
        },
        'required': {
            'value': True,
            'error_code': '119',
        },
    },
    'participants': {
        'type': {
            'value': 'string',
            'error_code': '1005',
        },
        'required': {
            'value': True,
            'error_code': '999',
        },
    },
    'pet': {
        'type': {
            'value': 'string',
            'error_code': '1000',
        },
        'regex': {
            'value': '^(None|CDC_DP|ThHE)$',
            'error_code': '1001',
        },
    },
    'model': {
        'type': {
            'value': 'string',
            'error_code': '1002',
        },
        'regex': {
            'value': '^(NN|NN_FHIR)$',
            'error_code': '1003',
        },
    },
    'legal': {
        'type': {
            'value': 'string',
            'error_code': '120',
        },
    },
    'study_privacy_budget': {
        'type': {
            'value': 'number',
            'error_code': '121',
        },
    },
    'expiration_date': {
        'type': {
            'value': 'timestamp',
            'error_code': '122',
        },
    },
    'study_id': {
        'type': {
            'value': 'number',
            'error_code': '123',
        },
    },
    'created_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '124',
        },
    },
    'updated_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '125',
        },
    },
    'created_by': {
        'type': {
            'value': 'number',
            'error_code': '126',
        },
    },
    'updated_by': {
        'type': {
            'value': 'number',
            'error_code': '127',
        },
    },
}
