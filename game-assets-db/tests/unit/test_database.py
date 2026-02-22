"""
单元测试 - 数据库操作
"""
import pytest
import sqlite3
from pathlib import Path
import sys

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app import init_db, get_db, DB_PATH


@pytest.fixture
def test_db(tmp_path):
    """创建临时测试数据库"""
    test_db_path = tmp_path / "test_assets.db"
    conn = sqlite3.connect(str(test_db_path))
    conn.row_factory = sqlite3.Row
    
    # 导入 schema
    schema = Path(__file__).parent.parent.parent / "schema.sql"
    with open(schema) as f:
        conn.executescript(f.read())
    
    yield conn
    
    conn.close()


class TestAssets:
    """素材 CRUD 测试"""
    
    def test_add_asset(self, test_db):
        """测试添加素材"""
        test_db.execute("""
            INSERT INTO assets (name, category, subcategory, tags, source_url, license)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("测试角色", "sprite", "character", "test,player", "https://test.com", "CC0"))
        test_db.commit()
        
        result = test_db.execute("SELECT * FROM assets WHERE name = ?", ("测试角色",)).fetchone()
        
        assert result is not None
        assert result["name"] == "测试角色"
        assert result["category"] == "sprite"
        assert result["license"] == "CC0"
    
    def test_update_asset(self, test_db):
        """测试更新素材"""
        # 先添加
        test_db.execute("""
            INSERT INTO assets (name, category, rating)
            VALUES (?, ?, ?)
        """, ("原素材", "sprite", 3))
        test_db.commit()
        asset_id = test_db.execute("SELECT id FROM assets WHERE name = ?", ("原素材",)).fetchone()["id"]
        
        # 再更新
        test_db.execute("""
            UPDATE assets SET name = ?, rating = ? WHERE id = ?
        """, ("新素材", 5, asset_id))
        test_db.commit()
        
        result = test_db.execute("SELECT * FROM assets WHERE id = ?", (asset_id,)).fetchone()
        
        assert result["name"] == "新素材"
        assert result["rating"] == 5
    
    def test_delete_asset(self, test_db):
        """测试删除素材"""
        # 先添加
        test_db.execute("INSERT INTO assets (name, category) VALUES (?, ?)", ("待删除", "sprite"))
        test_db.commit()
        asset_id = test_db.execute("SELECT id FROM assets WHERE name = ?", ("待删除",)).fetchone()["id"]
        
        # 删除
        test_db.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
        test_db.commit()
        
        result = test_db.execute("SELECT * FROM assets WHERE id = ?", (asset_id,)).fetchone()
        
        assert result is None
    
    def test_search_by_tag(self, test_db):
        """测试标签搜索"""
        # 清空表
        test_db.execute("DELETE FROM assets")
        test_db.commit()
        
        test_db.execute("INSERT INTO assets (name, category, tags) VALUES (?, ?, ?)", ("A", "sprite", "wheelchair,blue"))
        test_db.execute("INSERT INTO assets (name, category, tags) VALUES (?, ?, ?)", ("B", "sprite", "enemy,red"))
        test_db.commit()
        
        results = test_db.execute("SELECT * FROM assets WHERE tags LIKE ?", ("%wheelchair%",)).fetchall()
        
        assert len(results) == 1
        assert results[0]["name"] == "A"
    
    def test_filter_by_category(self, test_db):
        """测试分类筛选"""
        # 清空表
        test_db.execute("DELETE FROM assets")
        test_db.commit()
        
        test_db.execute("INSERT INTO assets (name, category) VALUES (?, ?)", ("A", "sprite"))
        test_db.execute("INSERT INTO assets (name, category) VALUES (?, ?)", ("B", "ui"))
        test_db.commit()
        
        results = test_db.execute("SELECT * FROM assets WHERE category = ?", ("sprite",)).fetchall()
        
        assert len(results) == 1
        assert results[0]["name"] == "A"


class TestDatabaseSchema:
    """数据库 Schema 测试"""
    
    def test_required_columns_exist(self, test_db):
        """测试必要列存在"""
        columns = [row["name"] for row in test_db.execute("PRAGMA table_info(assets)").fetchall()]
        
        required = ["id", "name", "category", "tags", "source_url", "license", "game_project"]
        for col in required:
            assert col in columns, f"Column {col} should exist"
    
    def test_category_index_exists(self, test_db):
        """测试索引存在"""
        indexes = [row["name"] for row in test_db.execute("PRAGMA index_list(assets)").fetchall()]
        
        assert "idx_category" in indexes


class TestBusinessLogic:
    """业务逻辑测试"""
    
    def test_default_license(self, test_db):
        """测试默认许可证"""
        test_db.execute("INSERT INTO assets (name, category) VALUES (?, ?)", ("测试", "sprite"))
        test_db.commit()
        
        result = test_db.execute("SELECT license FROM assets WHERE name = ?", ("测试",)).fetchone()
        
        assert result["license"] == "Unknown"
    
    def test_rating_range(self, test_db):
        """测试评分范围"""
        test_db.execute("INSERT INTO assets (name, category, rating) VALUES (?, ?, ?)", ("测试", "sprite", 5))
        test_db.commit()
        
        result = test_db.execute("SELECT rating FROM assets WHERE name = ?", ("测试",)).fetchone()
        
        assert 0 <= result["rating"] <= 5
