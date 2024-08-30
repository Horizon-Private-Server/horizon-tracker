from pydantic import BaseModel


class Pagination[T](BaseModel):
    count: int
    results: list[T]


class LeaderboardEntry(BaseModel):
    horizon_id: int
    name: str
    rank: int
    score: int
