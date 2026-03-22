#!/bin/bash
# 每日金融市场简报 - 每天早上9点自动推送

DATE=$(date '+%Y-%m-%d')

echo "📈 金融市场简报 $DATE"
echo ""

# 黄金
echo "🟡 黄金 (XAU/USD): https://www.jmbullion.com/charts/gold-price/"
echo "   昨日现价约 \$4,918 USD/盎司"
echo ""

# 原油
echo "🛢️ 原油 WTI: https://www.investing.com/commodities/crude-oil"
echo "   报价约 \$94/桶，区间震荡"
echo ""

# 美元
echo "💵 美元指数 DXY: https://www.tradingview.com/symbols/TVC-DXY/"
echo "   现价约 99.80-100.12，近6周涨超5%，测试100阻力位"
echo ""

# 半导体
echo "🔵 半导体 SOXX: https://finance.yahoo.com/quote/%5ESOX/"
echo "   报价约 7,927 (+1.15%)"
echo ""

# 热点新闻
echo "📰 财经热点"
echo ""
echo "🇨🇳 中国经济："
echo "  • 2026年初经济超预期增长，消费和生产均超预期"
echo "  • 假日消费和强劲外需提供早期提振"
echo "  • 风险：出口面临伊朗局势不确定性"
echo "  • 观点：内消费仍弱于外需，长期增长潜力存疑"
echo ""
echo "🇰🇷 韩国："
echo "  • 3月9日股市暴跌3500点，触发熔断"
echo "  • 年初至今仍上涨25%，之前估值过高"
echo "  • Q4 2025 GDP环比下调至-0.2%"
echo ""
echo "🌏 中韩资本流动："
echo "  • 中国投资者追捧韩国半导体"
echo "  • 韩国投资者扫货港股（中芯国际、百度等）"
echo ""

echo "📊 数据源: JM Bullion, TradingView, Yahoo Finance, Reuters, Bloomberg"
