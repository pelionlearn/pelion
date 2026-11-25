from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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

    result = await db.execute(
        select(Invitation).where(Invitation.id == invitation_id)
    )

    invitation = result.scalar_one_or_none()

    if invitation is None:
        raise errors.NotFoundError(f"Invitation {invitation_id} not found")

    if invitation.expires_at <= now:
        await delete_invitation(db, invitation_id)
        raise errors.NotFoundError(f"Invitation {invitation_id} expired")

    return invitation


async def delete_invitation(db: AsyncSession, invitation_id: UUID):
    invitation = await db.get(Invitation, invitation_id)

    # TODO: may be better not to raise error, more idempotent, error feedback for this isnt necessary
    if invitation is None:
        raise errors.NotFoundError(f"Invitation {invitation_id} not found")
    
    await db.delete(invitation)
    await db.flush()
    return invitation