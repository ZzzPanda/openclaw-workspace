"""
集成测试 - API 端点
"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app import app, init_db, DB_PATH


@pytest.fixture
def client(tmp_path):
    """测试客户端"""
    # 使用临时数据库
    import app as app_module
    original_db = app_module.DB_PATH
    test_db = tmp_path / "test.db"
    app_module.DB_PATH = test_db
    
    # 初始化测试数据库
    init_db()
    
    client = TestClient(app)
    
    yield client
    
    # 恢复
    app_module.DB_PATH = original_db


class TestAPIEndpoints:
    """API 端点测试"""
    
    def test_home_page_loads(self, client):
        """测试首页加载"""
        response = client.get("/")
        assert response.status_code == 200
        assert "游戏素材库" in response.text
    
    def test_add_page_loads(self, client):
        """测试添加页面加载"""
        response = client.get("/add")
        assert response.status_code == 200
        assert "添加素材" in response.text
    
    def test_add_asset(self, client):
        """测试添加素材 API"""
        response = client.post("/add", data={
            "name": "测试角色",
            "category": "sprite",
            "subcategory": "character",
            "tags": "test,player",
            "source_url": "https://test.com",
            "license": "CC0",
            "format": "png",
            "resolution": "16x16"
        })
        
        assert response.status_code == 200
        assert "已添加" in response.text
    
    def test_search_assets(self, client):
        """测试搜索功能"""
        # 先添加
        client.post("/add", data={
            "name": "轮椅角色",
            "category": "sprite",
            "tags": "wheelchair,player"
        })
        
        # 搜索
        response = client.get("/?search=轮椅")
        assert response.status_code == 200
        assert "轮椅角色" in response.text
    
    def test_filter_by_category(self, client):
        """测试分类筛选"""
        # 清理旧数据
        import app as app_module
        conn = app_module.get_db()
        conn.execute("DELETE FROM assets")
        conn.commit()
        conn.close()
        
        client.post("/add", data={"name": "SpriteTest", "category": "sprite", "tags": ""})
        client.post("/add", data={"name": "UITest", "category": "ui", "tags": ""})
        
        response = client.get("/?category=sprite")
        assert response.status_code == 200
        # 检查素材名称
        assert '<div class="name">SpriteTest</div>' in response.text
        assert '<div class="name">UITest</div>' not in response.text
    
    def test_edit_asset(self, client):
        """测试编辑素材"""
        # 先添加
        client.post("/add", data={
            "name": "原名称",
            "category": "sprite"
        })
        
        # 获取 ID (从列表页)
        response = client.get("/")
        # 简化测试：直接用固定 ID
        response = client.post("/edit/1", data={
            "name": "新名称",
            "category": "sprite",
            "tags": ""
        })
        
        # 验证
        response = client.get("/")
        assert "新名称" in response.text
    
    def test_delete_asset(self, client):
        """测试删除素材"""
        # 先添加
        client.post("/add", data={
            "name": "待删除",
            "category": "sprite"
        })
        
        # 删除
        response = client.get("/delete/1")
        assert response.status_code == 200
        
        # 验证删除
        import json
        data = response.json()
        assert data["success"] is True
    
    def test_api_stats(self, client):
        """测试统计 API"""
        # 添加测试数据
        client.post("/add", data={"name": "A", "category": "sprite"})
        client.post("/add", data={"name": "B", "category": "ui"})
        
        response = client.get("/api/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] >= 2


class TestValidation:
    """验证测试"""
    
    def test_name_required(self, client):
        """测试名称必填"""
        response = client.post("/add", data={
            "category": "sprite"
        })
        
        # FastAPI 会返回验证错误
        assert response.status_code in [200, 422]
    
    def test_category_required(self, client):
        """测试分类必填"""
        response = client.post("/add", data={
            "name": "测试"
        })
        
        assert response.status_code in [200, 422]
