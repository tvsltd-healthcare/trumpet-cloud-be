Datasets = {
    "id": {
        "type": {
            "value": "string",
            "error_code": "96"
        }
    },
    "name": {
        "required": {
            "value": True,
            "error_code": "97"
        },
        "max": {
            "value": 25,
            "error_code": "98"
        }
    },
    "meta_data": {
        "type": {
            "value": "text",
            "error_code": "99"
        },
        "required": {
            "value": True,
            "error_code": "100"
        }
    },
    "statistics": {
        "type": {
            "value": "text",
            "error_code": "101"
        }
    },
    "path": {
        "type": {
            "value": "text",
            "error_code": "102"
        }
    },
    # Todo: Fix Enum Issue
    "privacy_level": {
        "type": {
            "value": "string",
            "error_code": "104"
        },
        "regex": {
            "value": "^(public|confidential|highly_confidential)$",
            "error_code": "104"
        },
        "required": {
            "value": True,
            "error_code": "105"
        }
    },
    "created_at": {
        "type": {
            "value": "timestamp",
            "error_code": "106"
        }
    },
    "updated_at": {
        "type": {
            "value": "timestamp",
            "error_code": "107"
        }
    },
    "created_by": {
        "type": {
            "value": "number",
            "error_code": "108"
        }
    },
    "updated_by": {
        "type": {
            "value": "number",
            "error_code": "109"
        }
    }
}