from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from db.models import Invitation
from uuid import UUID
from exceptions import errors
from datetime import datetime, timedelta

async def create_invitation(
    db: AsyncSession, 
    classroom_id: UUID, 
    expires_in: timedelta = timedelta(days=7)
):
    invitation = Invitation(classroom_id=classroom_id, expires_at=datetime.now() + expires_in)

    db.add(invitation)
    await db.flush()
    await db.refresh(invitation)

    return invitation

async def get_valid_invitation(db: AsyncSession, invitation_id: UUID):
    now = datetime.now()

    result = await db.get(Invitation, invitation_id)

    invitation = result.scalar_one_or_none()

    if invitation is None:
        raise errors.NotFoundError(f"Invitation {invitation_id} not found or expired")

    if invitation.expires_at <= now:
        await delete_invitation(db, invitation_id)
        raise errors.NotFoundError(f"Invitation {invitation_id} expired")

    return invitation


async def delete_invitation(db: AsyncSession, invitation_id: UUID):
    invitation = await db.get(Invitation, invitation_id)

    if invitation is not None:
        await db.delete(invitation)
        await db.flush()

async def delete_expired_invitations(db: AsyncSession) -> int:
    now = datetime.now()

    stmt = delete(Invitation).where(Invitation.expires_at <= now)

    result = await db.execute(stmt)

    # commit this so it updates immediately
    await db.commit()

    return result.rowcount