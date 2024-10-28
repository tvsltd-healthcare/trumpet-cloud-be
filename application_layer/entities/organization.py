Organizations = {
    "id": {
        "type": {
            "value": "number",
            "error_code": "10"
        }
    },
    "name": {
        "type": {
            "value": "string",
            "error_code": "11"
        },
        "required": {
            "value": True,
            "error_code": "12"
        },
        "max": {
            "value": 30,
            "error_code": "13"
        }
    },
    "email": {
        "type": {
            "value": "string",
            "error_code": "14"
        },
        "required": {
            "value": True,
            "error_code": "15"
        },
        "max": {
            "value": 40,
            "error_code": "16"
        },
        "regex": {
            "value": "^[A-Za-z0-9._%-]@[A-Za-z0-9.-]\\\\.[A-Za-z]{2,}$",
            "error_code": "17"
        }
    },
    "address": {
        "type": {
            "value": "string",
            "error_code": "18"
        },
        "required": {
            "value": True,
            "error_code": "19"
        },
        "max": {
            "value": 50,
            "error_code": "20"
        }
    },
    "phone": {
        "type": {
            "value": "string",
            "error_code": "21"
        },
        "required": {
            "value": True,
            "error_code": "22"
        },
        "max": {
            "value": 20,
            "error_code": "23"
        }
    },
    "status": {
        "type": {
            "value": "string",
            "error_code": "24"
        },
        "regex": {
            "value": "^(approved|disapproved|blocked|pending_approval)$",
            "error_code": "25"
        },
        "required": {
            "value": True,
            "error_code": "26"
        }
    },
    "type": {
        "type": {
            "value": "string",
            "error_code": "27"
        },
        "regex": {
            "value": "^(data_owner|researcher)$",
            "error_code": "28"
        },
        "required": {
            "value": True,
            "error_code": "29"
        }
    },
    "created_at": {
        "type": {
            "value": "timestamp",
            "error_code": "30"
        }
    },
    "updated_at": {
        "type": {
            "value": "timestamp",
            "error_code": "31"
        }
    },
    "created_by": {
        "type": {
            "value": "number",
            "error_code": "32"
        }
    },
    "updated_by": {
        "type": {
            "value": "number",
            "error_code": "33"
        }
    }
}
