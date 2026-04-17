from email_service.templates.verify_org_email_template import VERIFY_ORG_EMAIL_TEMPLATE
from email_service.templates.reset_password_email_template import RESET_PASSWORD_EMAIL_TEMPLATE
from email_service.templates.verify_researcher_email_template import VERIFY_RESEARCHER_EMAIL_TEMPLATE
from email_service.templates.registration_approved_email_template import REGISTRATION_APPROVED_EMAIL_TEMPLATE
from email_service.templates.registration_disapproved_email_template import DISAPPROVED_REGISTRATION_EMAIL_TEMPLATE

EMAIL_TEMPLATE_MAP = {
    'verify_org': {
        'template': VERIFY_ORG_EMAIL_TEMPLATE,
        'subject': 'Organization verification on Trumpet Cloud'
    },
    'verify_researcher': {
        'template': VERIFY_RESEARCHER_EMAIL_TEMPLATE,
        'subject': 'Researcher verification on Trumpet Cloud'
    },
    'approved_registration': {
        'template': REGISTRATION_APPROVED_EMAIL_TEMPLATE,
        'subject': 'Your registration has been approved.'
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
