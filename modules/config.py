from dynaconf import Dynaconf, Validator


CONFIG_VALIDATORS = (
    Validator('github.user', must_exist=True),
    Validator('github.token', must_exist=True),
    Validator('github.repo', must_exist=True),
    Validator('github.branch', default='master'),
    Validator('github.min_date', default=None),
    Validator('github.max_date', default=None),
    Validator('github.top_users', default=30, gte=0),
    Validator('github.old_pr_age_days', default=30, gte=0),
    Validator('github.old_issue_age_days', default=14, gte=0),

    Validator('cache.conn_string', default='cache.pickle'),

    Validator('report.output_format', default='text', is_in=('json', 'text')),

    Validator('logging.formatters', default={}),
    Validator('logging.handlers', default={}),
    Validator('logging.loggers', default={}),
    Validator('logging.root', default={}),
    Validator('logging.version', default=1),
)

config = Dynaconf(
    environments=True,
    env_switcher='GITHUB_WATCHER_ENV',
    envvar_prefix='GITHUBWATCHER',
    merge_enabled=True,
    settings_files=['settings.yaml', '.secrets.yaml'],
    validators=CONFIG_VALIDATORS,
)
