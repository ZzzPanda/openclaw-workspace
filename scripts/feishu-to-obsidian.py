#!/usr/bin/env python3
"""
飞书文档同步到 Obsidian 工具
=============================
功能：
  1. 读取飞书文档 (通过 OpenClaw feishu_doc 工具)
  2. 转换为 Markdown
  3. 存入 Obsidian vault

使用方式：
  python feishu-to-obsidian.py --doc-token <token> [--vault-path <path>]

依赖：
  - OpenClaw 环境 (feishu_doc 工具)
  - Python 3.8+

调研结论：
  - 最佳方案：使用飞书 Open API + Markdown 转换
  - 已有工具参考：
    - feishu2md (GitHub: Wsine/feishu2md) - Go 实现的命令行工具
    - lark_docs_md - Python 库解析飞书文档
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ============ 配置 ============
DEFAULT_VAULT_PATH = "/Users/roger/Files/vault/panda"

# 飞书文档块类型到 Markdown 的映射
BLOCK_TYPE_MAP = {
    "text": "text",
    "heading1": "heading1",
    "heading2": "heading2", 
    "heading3": "heading3",
    "heading4": "heading4",
    "heading5": "heading5",
    "heading6": "heading6",
    "quote": "quote",
    "code": "code",
    "ordered_list": "ordered_list",
    "bulleted_list": "bulleted_list",
    "checklist": "checklist",
    "quote": "quote",
    "divider": "divider",
    "image": "image",
    "table": "table",
    "embed": "embed",
}


def call_feishu_doc_tool(action: str, **kwargs) -> dict:
    """
    通过子进程调用 OpenClaw 的 feishu_doc 工具
    
    注意：在 OpenClaw 环境中，应该直接导入工具函数
    这里提供一个框架，实际使用需要根据环境调整
    """
    # 方法1: 如果在 OpenClaw 环境中运行，可以直接 import
    # from feishu_doc import feishu_doc as feishu_doc_tool
    # return feishu_doc_tool(action=action, **kwargs)
    
    # 方法2: 通过命令行调用（需要先实现 CLI）
    # 这里只是框架，实际需要根据 OpenClaw 的调用方式调整
    
    raise NotImplementedError(
        "请在 OpenClaw 环境中直接调用 feishu_doc 工具函数"
    )


def convert_block_to_markdown(block: dict) -> str:
    """
    将飞书文档块转换为 Markdown 格式
    
    飞书文档块结构参考:
    {
        "type": "text",
        "text": {"content": "内容"},
        "heading1": {"text": {"content": "标题1"}},
        ...
    }
    """
    if not block:
        return ""
    
    block_type = block.get("type", "text")
    
    # 处理文本块
    if block_type == "text":
        text_obj = block.get("text", {})
        content = text_obj.get("content", "")
        return content
    
    # 处理标题
    if block_type.startswith("heading"):
        level = block_type[-1]  # 1-6
        text_obj = block.get(block_type, {}).get("text", {})
        content = text_obj.get("content", "")
        return f"{'#' * int(level)} {content}\n"
    
    # 处理引用
    if block_type == "quote":
        text_obj = block.get("quote", {}).get("text", {})
        content = text_obj.get("content", "")
        return f"> {content}\n"
    
    # 处理代码块
    if block_type == "code":
        code_obj = block.get("code", {})
        content = code_obj.get("content", "")
        language = code_obj.get("language", "")
        return f"```{language}\n{content}\n```\n"
    
    # 处理分隔线
    if block_type == "divider":
        return "---\n"
    
    # 处理图片
    if block_type == "image":
        image_obj = block.get("image", {})
        token = image_obj.get("token", "")
        return f"![飞书图片](https://open.feishu.cn/document/uc-api/smart-assistant/image/preview?file_token={token})\n"
    
    # TODO: 其他块类型处理
    print(f"⚠️  未处理的块类型: {block_type}")
    return ""


def convert_feishu_to_markdown(blocks: list) -> str:
    """
    将飞书文档块列表转换为完整 Markdown
    """
    markdown_lines = []
    
    for block in blocks:
        md_content = convert_block_to_markdown(block)
        if md_content:
            markdown_lines.append(md_content)
    
    return "\n".join(markdown_lines)


def sanitize_filename(title: str) -> str:
    """
    将文档标题转换为合法的文件名
    """
    # 替换非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', title)
    # 限制长度
    filename = filename[:200]
    return filename


def save_to_obsidian(markdown: str, title: str, vault_path: str) -> str:
    """
    将 Markdown 内容保存到 Obsidian vault
    """
    vault = Path(vault_path)
    
    # 确保 vault 存在
    if not vault.exists():
        raise FileNotFoundError(f"Obsidian vault 不存在: {vault_path}")
    
    # 生成文件名
    filename = sanitize_filename(title)
    if not filename.endswith(".md"):
        filename += ".md"
    
    file_path = vault / filename
    
    # 写入文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    return str(file_path)


def main():
    parser = argparse.ArgumentParser(
        description="飞书文档同步到 Obsidian"
    )
    parser.add_argument(
        "--doc-token", 
        required=True,
        help="飞书文档的 token (从 URL 中提取)"
    )
    parser.add_argument(
        "--vault-path",
        default=DEFAULT_VAULT_PATH,
        help=f"Obsidian vault 路径 (默认: {DEFAULT_VAULT_PATH})"
    )
    parser.add_argument(
        "--title",
        help="自定义文档标题 (默认使用飞书文档标题)"
    )
    
    args = parser.parse_args()
    
    print(f"📄 开始同步飞书文档...")
    print(f"   文档 Token: {args.doc_token}")
    print(f"   Vault 路径: {args.vault_path}")
    
    # 步骤1: 读取飞书文档
    # 注意: 这里需要通过 OpenClaw 工具调用
    # 由于 feishu_doc 是 OpenClaw 工具，需要在 OpenClaw 环境中调用
    # 下面的代码需要在 OpenClaw agent 会话中执行
    
    print("\n⚠️  注意: 此脚本需要在 OpenClaw 环境中运行")
    print("   请在 OpenClaw 会话中使用 feishu_doc 工具读取文档")
    print("   然后调用 convert_feishu_to_markdown() 转换")
    print("   最后调用 save_to_obsidian() 保存")
    
    # 示例代码框架 (在 OpenClaw 中执行):
    """
    # 1. 读取飞书文档
    doc_result = feishu_doc(action="read", doc_token="xxx")
    
    # 2. 获取文档标题和内容
    title = doc_result.get("title", "未命名文档")
    blocks = doc_result.get("blocks", [])
    
    # 3. 转换为 Markdown
    markdown = convert_feishu_to_markdown(blocks)
    
    # 4. 添加 frontmatter
    markdown_with_frontmatter = f'''---
title: {title}
feishu_token: {args.doc_token}
synced_at: {datetime.now().isoformat()}
---

{markdown}
'''
    
    # 5. 保存到 Obsidian
    file_path = save_to_obsidian(markdown_with_frontmatter, title, args.vault_path)
    print(f"✅ 已保存到: {file_path}")
    """
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
