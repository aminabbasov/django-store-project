LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{asctime} - {levelname} - {name}:{funcName}:{lineno}] - {message}',  # - {process:d} - {thread:d}
            'datefmt' : r"%y/%b/%Y %H:%M:%S",
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] - {message}',
            'style': '{',
        },
    },

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'app/logs/log.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        }
    },

    #! 'loggers': {
    #!     'website.views': {
    #!         'handlers': ['console', 'file', 'mail_admins'],
    #!         'level': 'DEBUG',
    #!     }
    #! }
}
