Files = {
    "id": {
        "type": {
            "value": "number",
            "error_code": "1"
        }
    },
    "type": {
        "type": {
            "value": "string",
            "error_code": "2"
        },
        "required": {
            "value": True,
            "error_code": "3"
        },
        "regex": {
            "value": "^(custom|legal|personal|other)$",
            "error_code": "4"
        }
    },
    "buffer": {
        "required": {
            "value": True,
            "error_code": "5"
        }
    },
    "created_at": {
        "type": {
            "value": "timestamp",
            "error_code": "6"
        }
    },
    "updated_at": {
        "type": {
            "value": "timestamp",
            "error_code": "7"
        }
    },
    "created_by": {
        "type": {
            "value": "number",
            "error_code": "8"
        }
    },
    "updated_by": {
        "required": {
            "value": "number",
            "error_code": "9"
        }
    }
}
