StudyAgreementResults = {
    'id': {
        'type': {
            'value': 'number',
            'error_code': '143',
        },
    },
    'study_agreement_id': {
        'type': {
            'value': 'number',
            'error_code': '144',
        },
    },
    'specification': {
        'type': {
            'value': 'text',
            'error_code': '145',
        },
        'required': {
            'value': 'true',
            'error_code': '146',
        },
    },
    'file_path': {
        'type': {
            'value': 'text',
            'error_code': '1004',
        },
    },
    'version': {
        'type': {
            'value': 'string',
            'error_code': '147',
        },
        'required': {
            'value': 'true',
            'error_code': '148',
        },
        'max': {
            'value': 20,
            'error_code': '149',
        },
    },
    'status': {
        'type': {
            'value': 'string',
            'error_code': '150',
        },
        'regex': {
            'value': '^(pending|completed)$',
            'error_code': '1501',
        },
        'required': {
            'value': 'true',
            'error_code': '151',
        },
    },
    'created_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '152',
        },
    },
    'updated_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '153',
        },
    },
    'created_by': {
        'type': {
            'value': 'number',
            'error_code': '154',
        },
    },
    'updated_by': {
        'type': {
            'value': 'number',
            'error_code': '155',
        },
    },
}
