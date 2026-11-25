from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from auth.authorization import require_classroom_member, require_classroom_owner
from auth.authentication import current_active_user
from db import repositories
from db.database import get_db
from schemas.users import UserRead

router = APIRouter(tags=["ClassMembers"])


@router.post("/classrooms/{classroom_id}/invitations")
async def create_invitation(
    classroom_id: UUID,
    _: None = Depends(require_classroom_owner),
    db: AsyncSession = Depends(get_db)
):
    invitation = await repositories.invitations.create_invitation(
        db,
        classroom_id,
    )
    return invitation.id

@router.get("/invitations/{invitation_id}/redeem")
async def redeem_invitation(
    invitation_id: UUID,
    user: None = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
):
    invitation = await repositories.invitations.get_valid_invitation(
        db, invitation_id
    )
    
    await repositories.classroom_members.add_classroom_member(
        db, invitation.classroom_id, user.id
    )