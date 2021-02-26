from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Type


@dataclass(frozen=True)
class StatsBaseModel:
    """Base model for various reports"""
    @classmethod
    def key(cls: Type) -> str:
        name = cls.__name__
        return name[0].lower() + name[1:]

    def to_table(self) -> List[str]:
        raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Contributor:
    name: str
    commit_count: int


@dataclass(frozen=True)
class ContributorStats(StatsBaseModel):
    contributors: List[Contributor]

    def to_table(self) -> List[str]:
        return [
            'Most active contributors:',
            '-------------------------',
            'Name' + (' ' * 20) + 'Commits',
        ] + [f'{c.name.ljust(24)}{c.commit_count}' for c in self.contributors]


@dataclass(frozen=True)
class PullRequestStats(StatsBaseModel):
    open_count: int
    closed_count: int
    old_count: int

    def to_table(self) -> List[str]:
        return [
            'Pull requests:',
            '--------------',
            'Open    Closed  Old',
            f'{str(self.open_count).ljust(8)}{str(self.closed_count).ljust(8)}{str(self.old_count).ljust(8)}'
        ]


@dataclass(frozen=True)
class IssueStats(StatsBaseModel):
    open_count: int
    closed_count: int
    old_count: int

    def to_table(self) -> List[str]:
        return [
            'Issues:',
            '-------',
            'Open    Closed  Old',
            f'{str(self.open_count).ljust(8)}{str(self.closed_count).ljust(8)}{str(self.old_count).ljust(8)}'
        ]
