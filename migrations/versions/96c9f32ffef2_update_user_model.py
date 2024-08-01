"""Update User model

Revision ID: 96c9f32ffef2
Revises: 9ab9cdc4adea
Create Date: 2024-07-31 18:58:19.940709

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '96c9f32ffef2'
down_revision = '9ab9cdc4adea'
branch_labels = None
depends_on = None

def upgrade():
    # Create Enum type
    user_roles = postgresql.ENUM('Admin', 'User', name='user_roles')
    user_roles.create(op.get_bind())

    # Update existing columns
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
    
    # Add new columns
    op.add_column('user', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('updated_at', sa.DateTime(), nullable=True))
    
    # Change role column type with USING clause
    op.execute('ALTER TABLE "user" ALTER COLUMN "role" TYPE user_roles USING role::user_roles')

def downgrade():
    # Revert role column type
    op.execute('ALTER TABLE "user" ALTER COLUMN "role" TYPE VARCHAR(20) USING role::VARCHAR(20)')
    
    # Remove new columns
    op.drop_column('user', 'updated_at')
    op.drop_column('user', 'created_at')
    
    # Revert password_hash column
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)
    
    # Drop Enum type
    user_roles = postgresql.ENUM('Admin', 'User', name='user_roles')
    user_roles.drop(op.get_bind())
