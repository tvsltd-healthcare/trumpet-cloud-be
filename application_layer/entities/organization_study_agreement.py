OrganizationStudyAgreements = {
    'id': {
        'type': {
            'value': 'number',
            'error_code': '7073',
        },
    },
    'study_agreement_id': {
        'type': {
            'value': 'number',
            'error_code': '7074',
        },
    },
    'organization_id': {
        'type': {
            'value': 'number',
            'error_code': '7075',
        },
    },
    'dataset_id': {
        'type': {
            'value': 'number',
            'error_code': '7086',
        },
    },
    'status': {
        'type': {
            'value': 'string',
            'error_code': '24',
        },
        'regex': {
            'value': '^(approved|disapproved|pending)$',
            'error_code': '7025',
        }
    },
    'created_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '7076',
        },
    },
    'updated_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '7077',
        },
    },
    'created_by': {
        'type': {
            'value': 'number',
            'error_code': '7078',
        },
    },
    'updated_by': {
        'type': {
            'value': 'number',
            'error_code': '7079',
        },
    },
}
