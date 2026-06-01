"""init_schema

Revision ID: cc31b4871e47
Revises: 
Create Date: 2026-05-31 01:38:11.536249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import os

# revision identifiers, used by Alembic.
revision: str = 'cc31b4871e47'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. 取得 schema.sql 的絕對路徑
    schema_path = os.path.join(os.path.dirname(__file__), '..', '..', 'schema.sql')
    
    # 2. 讀取 SQL 檔案內容
    with open(schema_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # 3. 讓 Alembic 執行這段 SQL，一口氣建立所有資料表
    connection = op.get_bind()
    connection.execute(sql_script)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP SCHEMA IF EXISTS ocpp CASCADE;")
    pass
