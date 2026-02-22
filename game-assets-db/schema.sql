-- 游戏素材数据库 Schema
-- SQLite 版本

CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                    -- 素材名称
    category TEXT NOT NULL,                 -- 分类: sprite, tileset, sound, music, font, effect, ui, other
    subcategory TEXT,                       -- 子分类: character, enemy, weapon, vehicle, etc.
    tags TEXT,                              -- 标签: comma separated
    source_url TEXT,                        -- 来源 URL (itch.io, freesound, etc.)
    local_path TEXT,                         -- 本地存储路径
    license TEXT DEFAULT 'Unknown',          -- 许可证: CC0, MIT, Free, Commercial, etc.
    format TEXT,                             -- 文件格式: png, wav, ogg, etc.
    resolution TEXT,                         -- 分辨率: 16x16, 32x32, 128x128, etc.
    color_style TEXT,                        -- 颜色风格: pixel, watercolor, vector, etc.
    game_project TEXT,                       -- 关联项目: WheelPower, etc.
    notes TEXT,                              -- 备注
    rating INTEGER DEFAULT 0,               -- 评分 1-5
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_category ON assets(category);
CREATE INDEX IF NOT EXISTS idx_subcategory ON assets(subcategory);
CREATE INDEX IF NOT EXISTS idx_tags ON assets(tags);
CREATE INDEX IF NOT EXISTS idx_game_project ON assets(game_project);

-- 示例数据
INSERT INTO assets (name, category, subcategory, tags, source_url, license, format, resolution, color_style, game_project, notes) VALUES
('轮椅角色', 'sprite', 'character', 'wheelchair,player,16x16', 'https://itch.io', 'CC0', 'png', '16x16', 'pixel', 'WheelPower', '主角轮椅'),
('激光枪', 'sprite', 'weapon', 'laser,gun,weapon', 'https://itch.io', 'CC0', 'png', '16x16', 'pixel', 'WheelPower', '玩家武器');
