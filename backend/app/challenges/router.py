"""
STARK INDUSTRIES SQL — Challenges Router
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from typing import List, Optional

from app.database import get_db
from app.auth.router import get_current_user
from app.auth.models import User, ChallengeProgress, AttackLog
from app.challenges.registry import get_challenge, get_all_challenges, CHALLENGES
from app.challenges.service import validate_flag, use_hint, get_user_stats

router = APIRouter(prefix="/challenges", tags=["challenges"])


class FlagSubmission(BaseModel):
    flag: str


class HintRequest(BaseModel):
    hint_number: int


@router.get("/")
async def list_challenges(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all challenges with user progress."""
    result = await db.execute(
        select(ChallengeProgress).where(ChallengeProgress.user_id == current_user.id)
    )
    progress_map = {p.challenge_id: p for p in result.scalars().all()}

    challenges_out = []
    for ch in get_all_challenges():
        p = progress_map.get(ch.challenge_id)
        ch_dict = ch.to_dict(include_flag=False)
        ch_dict["completed"] = p.completed if p else False
        ch_dict["hints_used"] = p.hints_used if p else 0
        ch_dict["attempts"] = p.attempts if p else 0
        ch_dict["xp_earned"] = p.xp_earned if p else 0
        challenges_out.append(ch_dict)

    return {"challenges": challenges_out}


@router.get("/{challenge_id}")
async def get_challenge_detail(
    challenge_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get challenge detail. Solution only shown if completed."""
    ch = get_challenge(challenge_id)
    if not ch:
        raise HTTPException(status_code=404, detail="Challenge not found")

    result = await db.execute(
        select(ChallengeProgress).where(
            ChallengeProgress.user_id == current_user.id,
            ChallengeProgress.challenge_id == challenge_id,
        )
    )
    progress = result.scalar_one_or_none()
    completed = progress.completed if progress else False

    ch_dict = ch.to_dict(include_flag=False)
    ch_dict["completed"] = completed
    ch_dict["hints_used"] = progress.hints_used if progress else 0
    ch_dict["attempts"] = progress.attempts if progress else 0
    ch_dict["xp_earned"] = progress.xp_earned if progress else 0

    # Only expose solution after completion
    if not completed:
        ch_dict["solution_explanation"] = None
        ch_dict["secure_code"] = None
        ch_dict["vulnerable_code"] = None

    return ch_dict


@router.post("/{challenge_id}/submit")
async def submit_flag(
    challenge_id: int,
    body: FlagSubmission,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit a flag for validation."""
    result = await validate_flag(db, current_user.id, challenge_id, body.flag)
    return result


@router.post("/{challenge_id}/hint")
async def get_hint(
    challenge_id: int,
    body: HintRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a hint for a challenge."""
    result = await use_hint(db, current_user.id, challenge_id, body.hint_number)
    return result


@router.get("/stats/me")
async def my_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_user_stats(db, current_user.id)


@router.get("/leaderboard/all")
async def leaderboard(db: AsyncSession = Depends(get_db)):
    """Public leaderboard — returns users sorted by XP."""
    result = await db.execute(
        select(User).order_by(desc(User.xp)).limit(50)
    )
    users = result.scalars().all()

    board = []
    for i, u in enumerate(users, 1):
        # Count completed challenges
        pr = await db.execute(
            select(ChallengeProgress).where(
                ChallengeProgress.user_id == u.id,
                ChallengeProgress.completed == True,
            )
        )
        completed_count = len(pr.scalars().all())
        board.append({
            "rank": i,
            "username": u.username,
            "xp": u.xp,
            "level": u.level,
            "rank_title": u.rank,
            "completed": completed_count,
        })

    return {"leaderboard": board}


@router.get("/logs/recent")
async def recent_logs(
    challenge_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 50,
):
    """Get recent attack log events."""
    query = select(AttackLog)
    if challenge_id:
        query = query.where(AttackLog.challenge_id == challenge_id)
    query = query.order_by(desc(AttackLog.timestamp)).limit(limit)
    result = await db.execute(query)
    logs = result.scalars().all()

    return {
        "logs": [
            {
                "id": l.id,
                "challenge_id": l.challenge_id,
                "event_type": l.event_type,
                "message": l.message,
                "timestamp": l.timestamp.isoformat() if l.timestamp else None,
            }
            for l in logs
        ]
    }
