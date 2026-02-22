#!/usr/bin/env python3
"""
游戏素材库 Web UI
运行: python app.py
访问: http://localhost:8000
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 配置
DB_PATH = Path(__file__).parent / "assets.db"
PORT = 8000

app = FastAPI(title="🎮 游戏素材库")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库"""
    if not DB_PATH.exists():
        conn = get_db()
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())
        conn.close()
        print(f"✅ 数据库已创建: {DB_PATH}")


# ============== 页面路由 ==============

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """首页 - 素材列表"""
    conn = get_db()
    
    # 获取筛选参数
    category = request.query_params.get("category")
    subcategory = request.query_params.get("subcategory")
    search = request.query_params.get("search")
    project = request.query_params.get("project")
    
    # 构建查询
    query = "SELECT * FROM assets WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = ?"
        params.append(category)
    if subcategory:
        query += " AND subcategory = ?"
        params.append(subcategory)
    if search:
        query += " AND (name LIKE ? OR tags LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    if project:
        query += " AND game_project = ?"
        params.append(project)
    
    query += " ORDER BY updated_at DESC"
    
    assets = conn.execute(query, params).fetchall()
    
    # 获取筛选选项
    categories = conn.execute("SELECT DISTINCT category FROM assets").fetchall()
    subcategories = conn.execute("SELECT DISTINCT subcategory FROM assets WHERE subcategory IS NOT NULL").fetchall()
    projects = conn.execute("SELECT DISTINCT game_project FROM assets WHERE game_project IS NOT NULL").fetchall()
    
    conn.close()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "assets": assets,
        "categories": categories,
        "subcategories": subcategories,
        "projects": projects,
        "filters": {"category": category, "subcategory": subcategory, "search": search, "project": project}
    })


@app.get("/add", response_class=HTMLResponse)
async def add_page(request: Request):
    """添加素材页面"""
    conn = get_db()
    categories = conn.execute("SELECT DISTINCT category FROM assets").fetchall()
    subcategories = conn.execute("SELECT DISTINCT subcategory FROM assets WHERE subcategory IS NOT NULL").fetchall()
    projects = conn.execute("SELECT DISTINCT game_project FROM assets WHERE game_project IS NOT NULL").fetchall()
    conn.close()
    
    return templates.TemplateResponse("add.html", {
        "request": request,
        "categories": categories,
        "subcategories": subcategories,
        "projects": projects
    })


@app.post("/add", response_class=HTMLResponse)
async def add_asset(
    name: str = Form(...),
    category: str = Form(...),
    subcategory: str = Form(None),
    tags: str = Form(None),
    source_url: str = Form(None),
    license: str = Form("Unknown"),
    format: str = Form(None),
    resolution: str = Form(None),
    color_style: str = Form(None),
    game_project: str = Form(None),
    notes: str = Form(None)
):
    """添加素材"""
    conn = get_db()
    conn.execute("""
        INSERT INTO assets (name, category, subcategory, tags, source_url, license, format, resolution, color_style, game_project, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, category, subcategory, tags, source_url, license, format, resolution, color_style, game_project, notes))
    conn.commit()
    conn.close()
    
    return templates.TemplateResponse("success.html", {"request": {}, "message": f"✅ 已添加: {name}"})


@app.get("/edit/{asset_id}", response_class=HTMLResponse)
async def edit_page(request: Request, asset_id: int):
    """编辑素材页面"""
    conn = get_db()
    asset = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,)).fetchone()
    categories = conn.execute("SELECT DISTINCT category FROM assets").fetchall()
    projects = conn.execute("SELECT DISTINCT game_project FROM assets WHERE game_project IS NOT NULL").fetchall()
    conn.close()
    
    return templates.TemplateResponse("edit.html", {
        "request": request,
        "asset": asset,
        "categories": categories,
        "projects": projects
    })


@app.post("/edit/{asset_id}", response_class=HTMLResponse)
async def edit_asset(
    asset_id: int,
    name: str = Form(...),
    category: str = Form(...),
    subcategory: str = Form(None),
    tags: str = Form(None),
    source_url: str = Form(None),
    license: str = Form("Unknown"),
    format: str = Form(None),
    resolution: str = Form(None),
    color_style: str = Form(None),
    game_project: str = Form(None),
    notes: str = Form(None)
):
    """编辑素材"""
    conn = get_db()
    conn.execute("""
        UPDATE assets SET 
            name=?, category=?, subcategory=?, tags=?, source_url=?, license=?,
            format=?, resolution=?, color_style=?, game_project=?, notes=?,
            updated_at=CURRENT_TIMESTAMP
        WHERE id=?
    """, (name, category, subcategory, tags, source_url, license, format, 
          resolution, color_style, game_project, notes, asset_id))
    conn.commit()
    conn.close()
    
    return templates.TemplateResponse("success.html", {"request": {}, "message": f"✅ 已更新: {name}"})


@app.get("/delete/{asset_id}")
async def delete_asset(asset_id: int):
    """删除素材"""
    conn = get_db()
    asset = conn.execute("SELECT name FROM assets WHERE id = ?", (asset_id,)).fetchone()
    if asset:
        conn.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": f"已删除: {asset['name']}"}
    conn.close()
    return {"success": False, "message": "素材不存在"}


@app.get("/api/stats")
async def api_stats():
    """API: 统计数据"""
    conn = get_db()
    stats = {
        "total": conn.execute("SELECT COUNT(*) FROM assets").fetchone()[0],
        "by_category": conn.execute("SELECT category, COUNT(*) as count FROM assets GROUP BY category").fetchall(),
        "by_project": conn.execute("SELECT game_project, COUNT(*) as count FROM assets WHERE game_project IS NOT NULL GROUP BY game_project").fetchall(),
    }
    conn.close()
    return stats


if __name__ == "__main__":
    import uvicorn
    init_db()
    print(f"🎮 素材库启动: http://localhost:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
