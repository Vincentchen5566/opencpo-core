from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

# 🌟 引進專案在 api/main.py 裡使用的全域非同步 db 連線物件
from state.postgres import db 

router = APIRouter()

# ── 數據模型 (Pydantic Models) ──────────────────────────────────────────
class SiteCreate(BaseModel):
    name: str                         # 站點名稱 (必填，如：格蘭威爾道充電站)
    address: Optional[str] = None     # 地址
    latitude: Optional[float] = None  # 緯度
    longitude: Optional[float] = None # 經度

class SiteResponse(BaseModel):
    id: UUID
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ── 路由接口 (Endpoints) ────────────────────────────────────────────────
@router.post("", response_model=SiteResponse)
async def create_site(site_data: SiteCreate):
    """
    營運後台專用：新增充電站點，數據將寫入 pgAdmin 中建好的 ocpp.sites 表
    """
    query = """
        INSERT INTO ocpp.sites (name, address, latitude, longitude)
        VALUES (:name, :address, :latitude, :longitude)
        RETURNING id, name, address, latitude, longitude, created_at;
    """
    try:
        # 使用專案原本採用的 Databases 庫進行非同步 SQL 寫入並獲取單筆結果
        result = await db.fetch_one(query, {
            "name": site_data.name,
            "address": site_data.address,
            "latitude": site_data.latitude,
            "longitude": site_data.longitude
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("", response_model=list[SiteResponse])
async def get_sites():
    """
    獲取所有站點列表，供後台網頁展示或下拉選單歸類使用
    """
    query = "SELECT id, name, address, latitude, longitude, created_at FROM ocpp.sites ORDER BY created_at DESC;"
    result = await db.fetch_all(query)
    return result