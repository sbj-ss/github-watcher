#!/usr/bin/env python3

from json import dumps as json_dumps
from logging.config import dictConfig as logging_dict_config

from modules.api_client import ApiClient
from modules.cache import PickledDictCache
from modules.config import config


def create_client():
    return ApiClient(
        user=config.github.user,
        token=config.github.token,
        repo=config.github.repo,
        branch=config.github.branch,
        min_date=config.github.min_date,
        max_date=config.github.max_date,
        cache=cache,
    )


if __name__ == '__main__':
    logging_dict_config(config.logging)
    cache = PickledDictCache(config.cache.conn_string)
    client = create_client()
    reports = (
        client.get_top_contributors(),
        client.get_pull_request_stats(),
        client.get_issue_stats(),
    )
    cache.save()
    if config.report.output_format == 'text':
        for r in reports:
            print('\n'.join(r.to_table()))
            print('\n')
    elif config.report.output_format == 'json':
        obj = {r.key(): r.to_dict() for r in reports}
        print(json_dumps(obj))
