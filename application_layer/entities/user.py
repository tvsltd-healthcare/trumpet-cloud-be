Users = {
    "id": {
        "type": {
            "value": "number",
            "error_code": "42"
        }
    },
    "first_name": {
        "type": {
            "value": "string",
            "error_code": "43"
        },
        "required": {
            "value": True,
            "error_code": "44"
        },
        "max": {
            "value": 15,
            "error_code": "45"
        }
    },
    "last_name": {
        "type": {
            "value": "string",
            "error_code": "46"
        },
        "required": {
            "value": True,
            "error_code": "47"
        },
        "max": {
            "value": 15,
            "error_code": "48"
        }
    },
    "email": {
        "type": {
            "value": "string",
            "error_code": "49"
        },
        "required": {
            "value": True,
            "error_code": "50"
        },
        "regex": {
            "value": "^[A-Za-z0-9._%-]@[A-Za-z0-9.-]\\\\.[A-Za-z]{2,}$",
            "error_code": "51"
        },
        "max": {
            "value": 40,
            "error_code": "52"
        }
    },
    "password": {
        "type": {
            "value": "string",
            "error_code": "53"
        },
        "required": {
            "value": True,
            "error_code": "54"
        },
        "max": {
            "value": 40,
            "error_code": "55"
        }
    },
    "status": {
        "type": {
            "value": "string",
            "error_code": "56"
        },
        "regex": {
            "value": "^(approved|disapproved|blocked|pending_registration)$",
            "error_code": "57"
        },
        "required": {
            "value": True,
            "error_code": "58"
        }
    },
    "phone": {
        "type": {
            "value": "string",
            "error_code": "59"
        },
        "required": {
            "value": True,
            "error_code": "60"
        },
        "max": {
            "value": 20,
            "error_code": "61"
        }
    },
    "created_at": {
        "type": {
            "value": "timestamp",
            "error_code": "62"
        }
    },
    "updated_at": {
        "type": {
            "value": "timestamp",
            "error_code": "63"
        }
    },
    "created_by": {
        "type": {
            "value": "number",
            "error_code": "64"
        }
    },
    "updated_by": {
        "type": {
            "value": "number",
            "error_code": "65"
        }
    }
}
