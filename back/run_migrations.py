from alembic.config import Config
from alembic import command
from pathlib import Path
import os

# Create a custom config
alembic_cfg = Config()
alembic_cfg.set_main_option("script_location", "migrations")
alembic_cfg.set_main_option("sqlalchemy.url", "postgresql+psycopg://streamapp:mylov2@localhost:5432/streamapp")

# Run the migration
command.upgrade(alembic_cfg, "head")
