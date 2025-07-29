StudyAgreements = {
    'id': {
        'type': {
            'value': 'number',
            'error_code': '117',
        },
    },
    'purpose': {
        'type': {
            'value': 'text',
            'error_code': '118',
        },
        'required': {
            'value': True,
            'error_code': '119',
        },
    },
    'use_case': {
        'type': {
            'value': 'string',
            'error_code': '9990',
        },
        'regex': {
            'value': '^(HNC|SBRT|NSCLC)$',
            'error_code': '95500',
        },
        'required': {
            'value': True,
            'error_code': '99890',
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
        'regex': {
            'value': '^\s*\d+\s*(,\s*\d+\s*)*$',
            'error_code': '111001',
        }
    },
    'samples': {
        'type': {
            'value': 'number',
            'error_code': '1006',
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
    'pet_config': {
        'type': {
            'value': 'text',
            'error_code': '1000',
        },
        'required': {
            'value': True,
            'error_code': '130',
        },
    },
    'model': {
        'type': {
            'value': 'string',
            'error_code': '1002',
        },
        'regex': {
            'value': '^(NN_HNC|NN_HNC_NECRO_JAW|NN_HNC_DYSPHAGIA|NN_HNC_ORAL_MUCOSITIS|REG_LOG_HNC|REG_LOG_HNC_NECRO_JAW|REG_LOG_HNC_DYSPHAGIA|REG_LOG_HNC_ORAL_MUCOSITIS)$',
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
    'status': {
        'type': {
            'value': 'string',
            'error_code': '5006',
        },
        'regex': {
            'value': '^(approved|disapproved|pending)$',
            'error_code': '5007',
        },
        'required': {
            'value': True,
            'error_code': '5008',
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
