"""
STARK INDUSTRIES SQL — Challenge Service
Flag validation, XP award, hint tracking, and achievements.
"""
import hmac
import hashlib
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.auth.models import User, ChallengeProgress, HintUsage, Achievement, AttackLog
from app.challenges.registry import get_challenge, CHALLENGES


RANK_THRESHOLDS = [
    (0, "Recruit"),
    (200, "Junior Analyst"),
    (500, "SQL Apprentice"),
    (1000, "Injection Specialist"),
    (2000, "Blind SQLi Hunter"),
    (3500, "Database Explorer"),
    (5000, "Red Team Operator"),
    (7500, "WAF Survivor"),
    (10000, "SQL Master"),
]

ACHIEVEMENTS = {
    "first_blood": {"name": "First Blood", "description": "Complete your first challenge"},
    "sql_beginner": {"name": "SQL Beginner", "description": "Complete 5 challenges"},
    "injection_specialist": {"name": "Injection Specialist", "description": "Complete all Core challenges"},
    "blind_sql_hunter": {"name": "Blind SQL Hunter", "description": "Complete both blind SQL challenges"},
    "database_explorer": {"name": "Database Explorer", "description": "Complete all 4 DB-specific challenges"},
    "waf_survivor": {"name": "WAF Survivor", "description": "Complete the WAF bypass challenge"},
    "second_order_specialist": {"name": "Second-Order Specialist", "description": "Complete both second-order challenges"},
    "sql_master": {"name": "SQL Master", "description": "Complete all 30 challenges"},
}


def _safe_compare(a: str, b: str) -> bool:
    """Constant-time string comparison to prevent timing attacks."""
    return hmac.compare_digest(a.encode(), b.encode())


def calculate_rank(xp: int) -> str:
    rank = "Recruit"
    for threshold, name in RANK_THRESHOLDS:
        if xp >= threshold:
            rank = name
    return rank


def calculate_level(xp: int) -> int:
    return max(1, xp // 500 + 1)


async def get_or_create_progress(
    db: AsyncSession, user_id: int, challenge_id: int
) -> ChallengeProgress:
    result = await db.execute(
        select(ChallengeProgress).where(
            ChallengeProgress.user_id == user_id,
            ChallengeProgress.challenge_id == challenge_id,
        )
    )
    progress = result.scalar_one_or_none()
    if not progress:
        progress = ChallengeProgress(user_id=user_id, challenge_id=challenge_id)
        db.add(progress)
        await db.flush()
    return progress


async def validate_flag(
    db: AsyncSession,
    user_id: int,
    challenge_id: int,
    submitted_flag: str,
) -> dict:
    """Validate a flag submission. Returns result dict."""
    challenge = get_challenge(challenge_id)
    if not challenge:
        return {"success": False, "message": "Challenge not found"}

    progress = await get_or_create_progress(db, user_id, challenge_id)

    # Track attempt
    progress.attempts = (progress.attempts or 0) + 1
    flags_submitted = progress.flags_submitted or []
    flags_submitted.append(submitted_flag)
    progress.flags_submitted = flags_submitted

    # Compare flags
    if not _safe_compare(submitted_flag.strip(), challenge.flag):
        await db.commit()
        await log_event(db, user_id, challenge_id, "FLAG_INCORRECT", f"Incorrect flag submitted: {submitted_flag[:20]}")
        return {"success": False, "message": "Incorrect flag. Keep trying!"}

    if progress.completed:
        return {"success": True, "message": "Already completed!", "xp_earned": 0, "already_completed": True}

    # Calculate XP with hint penalty
    hints_used = progress.hints_used or 0
    base_xp = challenge.points
    hint_penalty = hints_used * 10
    xp_earned = max(base_xp - hint_penalty, int(base_xp * 0.5))

    # Mark complete
    progress.completed = True
    progress.completed_at = datetime.now(timezone.utc)
    progress.xp_earned = xp_earned

    # Award XP to user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        user.xp = (user.xp or 0) + xp_earned
        user.rank = calculate_rank(user.xp)
        user.level = calculate_level(user.xp)

    await db.commit()

    # Check achievements
    new_achievements = await check_achievements(db, user_id)

    await log_event(db, user_id, challenge_id, "FLAG_CORRECT", "Flag successfully captured!")

    return {
        "success": True,
        "message": f"Flag accepted! +{xp_earned} XP",
        "xp_earned": xp_earned,
        "new_achievements": new_achievements,
        "rank": user.rank if user else None,
        "level": user.level if user else None,
        "total_xp": user.xp if user else None,
    }


async def use_hint(
    db: AsyncSession, user_id: int, challenge_id: int, hint_number: int
) -> dict:
    """Record hint usage and return hint text."""
    if hint_number not in (1, 2, 3):
        return {"success": False, "message": "Invalid hint number"}

    challenge = get_challenge(challenge_id)
    if not challenge:
        return {"success": False, "message": "Challenge not found"}

    # Check if already used
    result = await db.execute(
        select(HintUsage).where(
            HintUsage.user_id == user_id,
            HintUsage.challenge_id == challenge_id,
            HintUsage.hint_number == hint_number,
        )
    )
    existing = result.scalar_one_or_none()
    if not existing:
        hint = HintUsage(user_id=user_id, challenge_id=challenge_id, hint_number=hint_number)
        db.add(hint)
        progress = await get_or_create_progress(db, user_id, challenge_id)
        progress.hints_used = (progress.hints_used or 0) + 1
        await db.commit()

    hints = {1: challenge.hint_1, 2: challenge.hint_2, 3: challenge.hint_3}
    return {"success": True, "hint": hints[hint_number], "hint_number": hint_number}


async def check_achievements(db: AsyncSession, user_id: int) -> List[dict]:
    """Check and award new achievements."""
    result = await db.execute(
        select(ChallengeProgress).where(
            ChallengeProgress.user_id == user_id,
            ChallengeProgress.completed == True,
        )
    )
    completed = result.scalars().all()
    completed_ids = {p.challenge_id for p in completed}

    result2 = await db.execute(
        select(Achievement).where(Achievement.user_id == user_id)
    )
    existing = {a.achievement_id for a in result2.scalars().all()}

    new_achievements = []

    def award(ach_id: str):
        if ach_id not in existing:
            new_achievements.append({"id": ach_id, **ACHIEVEMENTS[ach_id]})
            ach = Achievement(
                user_id=user_id,
                achievement_id=ach_id,
                name=ACHIEVEMENTS[ach_id]["name"],
            )
            db.add(ach)

    if len(completed_ids) >= 1:
        award("first_blood")
    if len(completed_ids) >= 5:
        award("sql_beginner")
    if {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}.issubset(completed_ids):
        award("injection_specialist")
    if {5, 6}.issubset(completed_ids):
        award("blind_sql_hunter")
    if {27, 28, 29, 30}.issubset(completed_ids):
        award("database_explorer")
    if 23 in completed_ids:
        award("waf_survivor")
    if {8, 25}.issubset(completed_ids):
        award("second_order_specialist")
    if len(completed_ids) >= 30:
        award("sql_master")

    if new_achievements:
        await db.commit()

    return new_achievements


async def log_event(
    db: AsyncSession,
    user_id: Optional[int],
    challenge_id: int,
    event_type: str,
    message: str,
    metadata: dict = None,
):
    log = AttackLog(
        user_id=user_id,
        challenge_id=challenge_id,
        event_type=event_type,
        message=message,
        metadata=metadata or {},
    )
    db.add(log)
    await db.commit()


async def get_user_stats(db: AsyncSession, user_id: int) -> dict:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return {}

    result2 = await db.execute(
        select(ChallengeProgress).where(ChallengeProgress.user_id == user_id)
    )
    all_progress = result2.scalars().all()
    completed = [p for p in all_progress if p.completed]

    result3 = await db.execute(
        select(Achievement).where(Achievement.user_id == user_id)
    )
    achievements = result3.scalars().all()

    total_attempts = sum(p.attempts or 0 for p in all_progress)
    success_rate = (len(completed) / max(total_attempts, 1)) * 100

    return {
        "user_id": user_id,
        "username": user.username,
        "xp": user.xp,
        "level": user.level,
        "rank": user.rank,
        "total_challenges": len(CHALLENGES),
        "completed": len(completed),
        "remaining": len(CHALLENGES) - len(completed),
        "success_rate": round(success_rate, 1),
        "achievements": [{"id": a.achievement_id, "name": a.name} for a in achievements],
        "progress": [
            {
                "challenge_id": p.challenge_id,
                "completed": p.completed,
                "hints_used": p.hints_used,
                "attempts": p.attempts,
                "xp_earned": p.xp_earned,
            }
            for p in all_progress
        ],
    }
