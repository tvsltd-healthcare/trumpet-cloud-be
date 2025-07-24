Datasets = {
    'id': {
        'type': {
            'value': 'number',
            'error_code': '96',
        },
    },
    'don_uid': {
        'type': {
            'value': 'string',
            'error_code': '960',
        },
        'required': {
            'value': True,
            'error_code': '961',
        }
    },
    'organization_id': {
        'type': {
            'value': 'number',
            'error_code': '1080',
        },
    },
    'title': {
        'type': {
            'value': 'string',
            'error_code': '962',
        },
        'required': {
            'value': True,
            'error_code': '97',
        },
        'max': {
            'value': 100,
            'error_code': '98',
        },
    },
    'about': {
        'type': {
            'value': 'text',
            'error_code': '99',
        },
        'required': {
            'value': True,
            'error_code': '100',
        },
    },
    'use_case': {
        'type': {
            'value': 'string',
            'error_code': '9900',
        },
        'regex': {
            'value': '^(HNC|SBRT|NSCLC)$',
            'error_code': '2500',
        },
        'required': {
            'value': True,
            'error_code': '10000',
        },
    },
    'statistics': {
        'type': {
            'value': 'text',
            'error_code': '101',
        },
    },
    'temporal_coverage_start': {
        'type': {
            'value': 'timestamp',
            'error_code': '10011',
        },
    },
    'temporal_coverage_end': {
        'type': {
            'value': 'timestamp',
            'error_code': '10012',
        },
    },
    'geospatial_coverage': {
        'type': {
            'value': 'text',
            'error_code': '10013',
        },
    },
    'doi_citation': {
        'type': {
            'value': 'text',
            'error_code': '10014',
        },
    },
    'provenance': {
        'type': {
            'value': 'text',
            'error_code': '10015',
        },
    },
    'license_title': {
        'type': {
            'value': 'string',
            'error_code': '10016',
        },
    },
    'license_details': {
        'type': {
            'value': 'text',
            'error_code': '10017',
        },
    },
    'created_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '106',
        },
    },
    'updated_at': {
        'type': {
            'value': 'timestamp',
            'error_code': '107',
        },
    },
    'created_by': {
        'type': {
            'value': 'number',
            'error_code': '108',
        },
    },
    'updated_by': {
        'type': {
            'value': 'number',
            'error_code': '109',
        },
    },
}
