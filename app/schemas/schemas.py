from pydantic import BaseModel


class Pagination[T](BaseModel):
    count: int
    results: list[T]


class LeaderboardEntry(BaseModel):
    horizon_id: int
    username: str
    rank: int
    score: int
