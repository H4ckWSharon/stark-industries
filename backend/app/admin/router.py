"""
STARK INDUSTRIES SQL — Admin Router
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from typing import Optional

from app.database import get_db
from app.auth.router import get_admin_user
from app.auth.models import User, ChallengeProgress, HintUsage, AttackLog, Achievement
from app.challenges.registry import get_all_challenges

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/overview")
async def admin_overview(
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Admin dashboard overview."""
    result = await db.execute(select(func.count(User.id)))
    total_users = result.scalar()

    result2 = await db.execute(
        select(func.count(ChallengeProgress.id)).where(ChallengeProgress.completed == True)
    )
    total_completions = result2.scalar()

    result3 = await db.execute(select(func.count(AttackLog.id)))
    total_events = result3.scalar()

    result4 = await db.execute(select(func.count(HintUsage.id)))
    total_hints = result4.scalar()

    return {
        "total_users": total_users,
        "total_completions": total_completions,
        "total_challenges": len(get_all_challenges()),
        "total_events": total_events,
        "total_hints_used": total_hints,
    }


@router.get("/students")
async def list_students(
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List all student accounts with progress summary."""
    result = await db.execute(select(User).order_by(desc(User.xp)))
    users = result.scalars().all()

    students = []
    for u in users:
        pr = await db.execute(
            select(func.count(ChallengeProgress.id)).where(
                ChallengeProgress.user_id == u.id,
                ChallengeProgress.completed == True,
            )
        )
        completed = pr.scalar()

        attempts_r = await db.execute(
            select(func.sum(ChallengeProgress.attempts)).where(
                ChallengeProgress.user_id == u.id
            )
        )
        total_attempts = attempts_r.scalar() or 0

        students.append({
            "id": u.id,
            "username": u.username,
            "xp": u.xp,
            "level": u.level,
            "rank": u.rank,
            "completed_challenges": completed,
            "total_attempts": total_attempts,
            "last_login": u.last_login.isoformat() if u.last_login else None,
        })

    return {"students": students}


@router.get("/students/{user_id}/progress")
async def student_progress(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Detailed progress for a specific student."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result2 = await db.execute(
        select(ChallengeProgress).where(ChallengeProgress.user_id == user_id)
    )
    progress = result2.scalars().all()

    result3 = await db.execute(
        select(Achievement).where(Achievement.user_id == user_id)
    )
    achievements = result3.scalars().all()

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "xp": user.xp,
            "level": user.level,
            "rank": user.rank,
        },
        "progress": [
            {
                "challenge_id": p.challenge_id,
                "completed": p.completed,
                "completed_at": p.completed_at.isoformat() if p.completed_at else None,
                "hints_used": p.hints_used,
                "attempts": p.attempts,
                "xp_earned": p.xp_earned,
            }
            for p in progress
        ],
        "achievements": [{"id": a.achievement_id, "name": a.name, "earned_at": a.earned_at.isoformat()} for a in achievements],
    }


@router.get("/logs")
async def admin_logs(
    challenge_id: Optional[int] = None,
    user_id: Optional[int] = None,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
):
    """Attack logs for admin review."""
    query = select(AttackLog).order_by(desc(AttackLog.timestamp)).limit(limit)
    if challenge_id:
        query = query.where(AttackLog.challenge_id == challenge_id)
    if user_id:
        query = query.where(AttackLog.user_id == user_id)

    result = await db.execute(query)
    logs = result.scalars().all()

    return {
        "logs": [
            {
                "id": l.id,
                "user_id": l.user_id,
                "challenge_id": l.challenge_id,
                "event_type": l.event_type,
                "message": l.message,
                "timestamp": l.timestamp.isoformat() if l.timestamp else None,
            }
            for l in logs
        ]
    }


@router.get("/challenges/stats")
async def challenge_stats(
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Per-challenge completion statistics."""
    result = await db.execute(
        select(
            ChallengeProgress.challenge_id,
            func.count(ChallengeProgress.id).label("total_attempts"),
            func.sum(func.cast(ChallengeProgress.completed, db.bind.dialect.Integer if hasattr(db, 'bind') else 'Integer')).label("completions"),
        ).group_by(ChallengeProgress.challenge_id)
    )
    # Simple approach
    result2 = await db.execute(select(ChallengeProgress))
    all_progress = result2.scalars().all()

    stats = {}
    for p in all_progress:
        cid = p.challenge_id
        if cid not in stats:
            stats[cid] = {"challenge_id": cid, "total_attempts": 0, "completions": 0, "hints_used": 0}
        stats[cid]["total_attempts"] += (p.attempts or 0)
        if p.completed:
            stats[cid]["completions"] += 1
        stats[cid]["hints_used"] += (p.hints_used or 0)

    return {"challenge_stats": list(stats.values())}
