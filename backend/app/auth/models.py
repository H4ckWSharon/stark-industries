"""
STARK INDUSTRIES SQL — Auth Models
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    rank = Column(String(50), default="Recruit")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))



class ChallengeProgress(Base):
    __tablename__ = "challenge_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    challenge_id = Column(Integer, nullable=False, index=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    hints_used = Column(Integer, default=0)
    attempts = Column(Integer, default=0)
    xp_earned = Column(Integer, default=0)
    flags_submitted = Column(JSON, default=list)


class HintUsage(Base):
    __tablename__ = "hint_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    challenge_id = Column(Integer, nullable=False)
    hint_number = Column(Integer, nullable=False)
    used_at = Column(DateTime(timezone=True), server_default=func.now())


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    achievement_id = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())


class AttackLog(Base):
    __tablename__ = "attack_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    challenge_id = Column(Integer, nullable=False)
    event_type = Column(String(50), nullable=False)
    message = Column(String(500))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    event_metadata = Column(JSON, default=dict)
