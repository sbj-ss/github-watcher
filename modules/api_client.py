from dataclasses import dataclass, field
from datetime import date
from logging import getLogger
from typing import Any, Dict, Optional, cast

from requests import Response, Session

from .cache import CacheBase
from .models import Contributor, ContributorStats, IssueStats, PullRequestStats


@dataclass(frozen=True)
class ApiResponse:
    etag: Optional[str]
    last_modified: Optional[str]
    payload: Any


@dataclass
class ApiClient:
    cache: CacheBase
    repo: str
    user: str
    token: str
    branch: str = 'master'
    min_date: Optional[date] = None
    max_date: Optional[date] = None
    logger: Any = field(init=False)
    session: Session = field(init=False)
    limit_remaining: int = field(init=False, default=-1)

    def __post_init__(self) -> None:
        self.logger = getLogger()
        self.session = Session()
        self.session.auth = (self.user, self.token)

    def _request(self, method: str, url: str, query: Dict[str, str]) -> Any:
        key: str = url + str(query)
        prev: ApiResponse = cast(ApiResponse, self.cache.get(key))
        headers: Dict[str, str] = {}
        if prev:
            if prev.etag:
                headers = {'If-None-Match': f'"{prev.etag}"'}
            elif prev.last_modified:
                headers = {'If-Modified-Since': prev.last_modified}
        response: Response = self.session.request(method, url, params=query, headers=headers)
        if response.status_code == 304:
            return prev.payload
        if response.ok:
            self.cache[key] = ApiResponse(
                etag=response.headers.get('ETag'),
                last_modified=response.headers.get('Last-Modified'),
                payload=response.json(),
            )
            self.limit_remaining = int(response.headers['X-RateLimit-Remaining'])
            return self.cache[key].payload
        self.logger.error('Can\'t fetch %s: %s' % (response.url, response.reason))
        return None

    def get_top_contributors(self) -> ContributorStats:
        return ContributorStats([Contributor('sbj-ss', 1)])

    def get_pull_request_stats(self) -> PullRequestStats:
        return PullRequestStats(open_count=0, closed_count=1, old_count=0)

    def get_issue_stats(self) -> IssueStats:
        return IssueStats(open_count=0, closed_count=1, old_count=0)
