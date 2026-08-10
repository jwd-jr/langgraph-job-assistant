from typing import TypedDict, List

class JobSearchState(TypedDict):
    query: str
    jobs: List[dict]
    resume_text: str
    scored_jobs: List[dict]
    retry_count: int
    tracked_jobs: List[dict]