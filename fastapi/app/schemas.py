from pydantic import BaseModel, ConfigDict, Field


class SkillData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill: str = Field(min_length=1)
    level: str = Field(min_length=1)


class MatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: int = Field(ge=1)
    teach: list[SkillData] = Field(default_factory=list)
    learn: list[SkillData] = Field(default_factory=list)


class MatchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: int = Field(ge=1)
    score: float = Field(ge=0, le=100)


class MatchResponse(BaseModel):
    matches: list[MatchResult] = Field(default_factory=list)