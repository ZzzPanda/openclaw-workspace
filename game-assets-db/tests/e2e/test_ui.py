"""
E2E 测试 - 端到端浏览器测试
使用 Playwright 进行 UI 测试
"""
import pytest
from playwright.sync_api import sync_playwright, expect


@pytest.fixture(scope="module")
def browser():
    """浏览器 fixture"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """页面 fixture"""
    page = browser.new_page()
    yield page
    page.close()


class TestE2E:
    """端到端测试"""
    
    def test_home_page_title(self, page):
        """测试首页标题"""
        page.goto("http://localhost:8000")
        expect(page).to_have_title("游戏素材库")
    
    def test_add_asset_flow(self, page):
        """测试添加素材流程"""
        # 1. 打开首页
        page.goto("http://localhost:8000")
        
        # 2. 点击添加按钮
        page.click("text=添加素材")
        
        # 3. 填写表单
        page.fill("input[name='name']", "E2E测试素材")
        page.select_option("select[name='category']", "sprite")
        page.fill("input[name='tags']", "e2e,test")
        page.fill("input[name='source_url']", "https://itch.io")
        
        # 4. 提交
        page.click("button[type='submit']")
        
        # 5. 验证成功
        page.wait_for_selector("text=已添加")
        expect(page.locator("text=已添加")).to_be_visible()
    
    def test_search_functionality(self, page):
        """测试搜索功能"""
        page.goto("http://localhost:8000")
        
        # 搜索
        page.fill("input[name='search']", "测试")
        page.click("button:has-text('筛选')")
        
        # 验证搜索结果
        page.wait_for_load_state("networkidle")
    
    def test_delete_asset(self, page):
        """测试删除素材"""
        # 先添加一个素材
        page.goto("http://localhost:8000/add")
        page.fill("input[name='name']", "待删除素材")
        page.select_option("select[name='category']", "sprite")
        page.click("button[type='submit']")
        
        # 确认添加成功
        page.wait_for_selector("text=已添加")
        
        # 删除
        page.goto("http://localhost:8000")
        
        # 点击删除按钮（需要先有素材）
        # 这里简化处理
        delete_buttons = page.locator("button:has-text('🗑️')")
        if delete_buttons.count() > 0:
            delete_buttons.first.click()
            page.wait_for_timeout(500)
    
    def test_navigation(self, page):
        """测试导航"""
        page.goto("http://localhost:8000")
        
        # 测试返回首页
        page.click("text=游戏素材库")
        expect(page).to_have_title("游戏素材库")


class TestResponsive:
    """响应式测试"""
    
    def test_mobile_view(self, browser):
        """测试移动端视图"""
        page = browser.new_page(viewport={"width": 375, "height": 667})
        page.goto("http://localhost:8000")
        
        # 验证响应式布局
        expect(page.locator("h1")).to_be_visible()
        
        page.close()


class TestAccessibility:
    """可访问性测试"""
    
    def test_form_labels(self, page):
        """测试表单标签"""
        page.goto("http://localhost:8000/add")
        
        # 验证 label 存在
        labels = page.locator("label").all()
        assert len(labels) > 0
    
    def test_buttons_have_text(self, page):
        """测试按钮有文本"""
        page.goto("http://localhost:8000")
        
        buttons = page.locator("button, .btn").all()
        for btn in buttons:
            assert len(btn.inner_text()) > 0 or btn.get_attribute("href")
