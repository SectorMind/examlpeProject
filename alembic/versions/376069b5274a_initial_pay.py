"""Initial pay

Revision ID: 376069b5274a
Revises: 3016f5be6827
Create Date: 2024-07-09 15:29:32.455182

"""
from typing import Sequence, Union

from alembic_postgresql_enum import TableReference
from sqlalchemy.dialects import postgresql
import fastapi_users_db_sqlalchemy.generics
import sqlalchemy_utils.types.email

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '376069b5274a'
down_revision: Union[str, None] = '3016f5be6827'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('user',
                    sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
                    sa.Column('user_name', sa.String(length=255), nullable=False),
                    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
                    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=False),
                    sa.Column('phone_number', sqlalchemy_utils.types.phone_number.PhoneNumberType(length=20),
                              nullable=True),
                    sa.Column('role',
                              postgresql.ENUM('ADMIN', 'MODERATOR', 'VIEWER', name='userrole', create_type=False),
                              nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('is_superuser', sa.Boolean(), nullable=False),
                    sa.Column('is_verified', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('phone_number'),
                    sa.UniqueConstraint('user_name')
                    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.sync_enum_values('public', 'userrole', ['ADMIN', 'MODERATOR', 'VIEWER'],
                        [TableReference(table_schema='public', table_name='user', column_name='role')])
    # ### end Alembic commands ###


def downgrade() -> None:
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # sa.Enum('ADMIN', 'MODERATOR', 'VIEWER', name='userrole').create(op.get_bind())
    # sa.Enum('ADMIN', 'MODERATOR', 'VIEWER', name='"UserRole"').create(op.get_bind())
    # ### end Alembic commands ###
