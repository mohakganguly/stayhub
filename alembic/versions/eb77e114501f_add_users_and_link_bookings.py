"""add users and link bookings

Revision ID: eb77e114501f
Revises: a62865410c61
Create Date: 2026-09-29 16:35:43.637604

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "eb77e114501f"
down_revision: Union[str, Sequence[str], None] = "a62865410c61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------------------------------------------------------
    # 1. Create users table
    # ---------------------------------------------------------

    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "email",
            name="uq_users_email",
        ),
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=False,
    )

    op.create_index(
        "ix_users_id",
        "users",
        ["id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # 2. Add user_id to existing bookings
    # ---------------------------------------------------------

    op.add_column(
        "bookings",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_bookings_user_id",
        "bookings",
        ["user_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_bookings_user_id_users",
        "bookings",
        "users",
        ["user_id"],
        ["id"],
    )

    # ---------------------------------------------------------
    # 3. Create users for existing guests
    # ---------------------------------------------------------

    connection = op.get_bind()

    existing_guests = connection.execute(
        sa.text(
            """
            SELECT DISTINCT guest_name
            FROM bookings
            WHERE guest_name IS NOT NULL
            """
        )
    ).fetchall()

    for row in existing_guests:
        guest_name = row[0]

        email = (
            guest_name.lower()
            .replace(" ", ".")
            + "@example.com"
        )

        connection.execute(
            sa.text(
                """
                INSERT INTO users (
                    name,
                    email,
                    password_hash
                )
                VALUES (
                    :name,
                    :email,
                    :password_hash
                )
                ON CONFLICT (email) DO NOTHING
                """
            ),
            {
                "name": guest_name,
                "email": email,
                "password_hash": "TEMPORARY_MIGRATION_HASH",
            },
        )

    # ---------------------------------------------------------
    # 4. Link existing bookings to users
    # ---------------------------------------------------------

    connection.execute(
        sa.text(
            """
            UPDATE bookings AS b
            SET user_id = u.id
            FROM users AS u
            WHERE u.name = b.guest_name
            """
        )
    )

    # ---------------------------------------------------------
    # 5. Make user_id mandatory
    # ---------------------------------------------------------

    op.alter_column(
        "bookings",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    # ---------------------------------------------------------
    # 6. Remove old guest_name column
    # ---------------------------------------------------------

    op.drop_column(
        "bookings",
        "guest_name",
    )


def downgrade() -> None:
    # ---------------------------------------------------------
    # 1. Restore guest_name
    # ---------------------------------------------------------

    op.add_column(
        "bookings",
        sa.Column(
            "guest_name",
            sa.String(length=100),
            nullable=True,
        ),
    )

    # Restore names from users.
    connection = op.get_bind()

    connection.execute(
        sa.text(
            """
            UPDATE bookings AS b
            SET guest_name = u.name
            FROM users AS u
            WHERE b.user_id = u.id
            """
        )
    )

    # Make guest_name mandatory again.
    op.alter_column(
        "bookings",
        "guest_name",
        existing_type=sa.String(length=100),
        nullable=False,
    )

    # ---------------------------------------------------------
    # 2. Remove foreign key and user_id
    # ---------------------------------------------------------

    op.drop_constraint(
        "fk_bookings_user_id_users",
        "bookings",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_bookings_user_id",
        table_name="bookings",
    )

    op.drop_column(
        "bookings",
        "user_id",
    )

    # ---------------------------------------------------------
    # 3. Remove users table
    # ---------------------------------------------------------

    op.drop_index(
        "ix_users_id",
        table_name="users",
    )

    op.drop_index(
        "ix_users_email",
        table_name="users",
    )

    op.drop_table("users")