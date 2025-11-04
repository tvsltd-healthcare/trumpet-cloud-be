from email_service.templates.varify_org_email_template import VARIFY_ORG_EMAIL_TEMPLATE
from email_service.templates.reset_password_email_template import RESET_PASSWORD_EMAIL_TEMPLATE
from email_service.templates.varify_researcher_email_template import VARIFY_RESEARCHER_EMAIL_TEMPLATE
from email_service.templates.registration_approved_email_templlate import REGISTRATION_APPROVED_EMAIL_TEMPLATE
from email_service.templates.registration_disapproved_email_templlate import DISAPPROVED_REGISTRATION_EMAIL_TEMPLATE

EMAIL_TEMPLATE_MAP = {
    'varify_org': {
        'template': VARIFY_ORG_EMAIL_TEMPLATE,
        'subject': 'Verify your organization on Trumpet Cloud'
    },
    'varify_researcher': {
        'template': VARIFY_RESEARCHER_EMAIL_TEMPLATE,
        'subject': 'Verify your researcher on Trumpet Cloud'
    },
    'approved_registration': {
        'template': REGISTRATION_APPROVED_EMAIL_TEMPLATE,
        'subject': 'Your registration has been successfully approved.'
    },
    'disapproved_registration': {
        'template': DISAPPROVED_REGISTRATION_EMAIL_TEMPLATE,
        'subject': 'Your registration has not been approved'
    },
    'reset_password': {
        'template': RESET_PASSWORD_EMAIL_TEMPLATE,
        'subject': 'Reset password.'
    }
}
