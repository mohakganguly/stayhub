"""add property data constraints

Revision ID: b9a78001b653
Revises: 947c3b69fa5a
Create Date: 2026-09-29 02:14:15.390048

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "b9a78001b653"
down_revision = "947c3b69fa5a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_check_constraint(
        "ck_properties_price_positive",
        "properties",
        "price_per_night > 0",
    )

    op.create_check_constraint(
        "ck_properties_max_guests_positive",
        "properties",
        "max_guests > 0",
    )

    op.create_check_constraint(
        "ck_properties_rating_range",
        "properties",
        "rating >= 0 AND rating <= 5",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "ck_properties_rating_range",
        "properties",
        type_="check",
    )

    op.drop_constraint(
        "ck_properties_max_guests_positive",
        "properties",
        type_="check",
    )

    op.drop_constraint(
        "ck_properties_price_positive",
        "properties",
        type_="check",
    )

