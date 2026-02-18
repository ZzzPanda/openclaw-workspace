#!/usr/bin/env node

/**
 * 全球金融市场数据抓取脚本
 * 使用免费 API 获取 A股、美股、港股、加密货币、黄金白银、汇率
 * 
 * 使用方法: node market-data.js
 */

const https = require('https');

// 颜色输出
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[36m',
  reset: '\x1b[0m'
};

function formatChange(change) {
  const num = parseFloat(change);
  if (num > 0) return `${colors.green}+${num.toFixed(2)}%${colors.reset} 📈`;
  if (num < 0) return `${colors.red}${num.toFixed(2)}%${colors.reset} 📉`;
  return `${colors.yellow}${num.toFixed(2)}%${colors.reset}`;
}

function fetch(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch(e) {
          resolve(data);
        }
      });
    });
    req.on('error', reject);
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('Timeout'));
    });
  });
}

async function getCrypto() {
  console.log(`\n${colors.blue}=== 加密货币 ===${colors.reset}`);
  try {
    const [btc, eth] = await Promise.all([
      fetch('https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT'),
      fetch('https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT')
    ]);
    console.log(`Bitcoin: $${parseInt(btc.lastPrice)} ${formatChange(btc.priceChangePercent)}`);
    console.log(`Ethereum: $${parseFloat(eth.lastPrice).toFixed(2)} ${formatChange(eth.priceChangePercent)}`);
  } catch(e) {
    console.log('加密货币 API 获取失败');
  }
}

async function getGold() {
  console.log(`\n${colors.blue}=== 贵金属 ===${colors.reset}`);
  try {
    // 使用 GoldAPI.io (免费版需要注册，这里用替代方案)
    // 这里用一个公开的贵金属价格页面
    const data = await fetch('https://api.metalpriceapi.com/v1/latest?api_key=demo&unit=toz&currency=USD');
    if (data.errors) {
      console.log('贵金属 API 需要 API Key');
    }
  } catch(e) {
    console.log('贵金属数据获取失败');
  }
}

async function getRMBRate() {
  console.log(`\n${colors.blue}=== 人民币汇率 ===${colors.reset}`);
  try {
    // 使用 exchangerate.host (免费)
    const data = await fetch('https://api.exchangerate.host/latest?base=CNY&symbols=USD,EUR,JPY,GBP');
    if (data.rates) {
      console.log(`美元 (USD): ¥${(1/data.rates.USD).toFixed(4)}`);
      console.log(`欧元 (EUR): ¥${(1/data.rates.EUR).toFixed(4)}`);
      console.log(`日元 (JPY): ¥${(1/data.rates.JPY*100).toFixed(4)}`);
      console.log(`英镑 (GBP): ¥${(1/data.rates.GBP).toFixed(4)}`);
    }
  } catch(e) {
    console.log('汇率获取失败');
  }
}

async function getChinaStock() {
  console.log(`\n${colors.blue}=== A股 ===${colors.reset}`);
  try {
    // 使用新浪财经 API
    const res = await fetch('https://hq.sinajs.cn/list=sh000001,sz399001');
    const lines = res.split('\n');
    
    const parseSina = (line) => {
      const match = line.match(/="([^"]+)"/);
      if (!match) return null;
      const parts = match[1].split(',');
      return {
        open: parseFloat(parts[1]),
        high: parseFloat(parts[2]),
        low: parseFloat(parts[3]),
        price: parseFloat(parts[4]),
        volume: parseFloat(parts[5]) / 100000000
      };
    };
    
    lines.forEach(line => {
      if (line.includes('sh000001')) {
        const data = parseSina(line);
        if (data) console.log(`上证指数: ${data.price.toFixed(2)}`);
      }
      if (line.includes('sz399001')) {
        const data = parseSina(line);
        if (data) console.log(`深证成指: ${data.price.toFixed(2)}`);
      }
    });
  } catch(e) {
    console.log('A股数据获取失败');
  }
}

async function getHKStock() {
  console.log(`\n${colors.blue}=== 港股 ===${colors.reset}`);
  try {
    const res = await fetch('https://api.twelvedata.com/time_series?symbol=HSI&interval=1day&apikey=demo');
    if (res.values && res.values[0]) {
      console.log(`恒生指数: ${parseFloat(res.values[0].close).toFixed(2)}`);
    }
  } catch(e) {
    console.log('港股数据获取失败');
  }
}

async function getUSStock() {
  console.log(`\n${colors.blue}=== 美股 ===${colors.reset}`);
  try {
    // 使用 Twelve Data 免费 API (demo key)
    const symbols = ['SPX', 'DJI', 'IXIC'];
    const names = ['S&P 500', '道琼斯', '纳斯达克'];
    
    for (let i = 0; i < symbols.length; i++) {
      try {
        const res = await fetch(`https://api.twelvedata.com/time_series?symbol=${symbols[i]}&interval=1day&apikey=demo`);
        if (res.values && res.values[0]) {
          console.log(`${names[i]}: ${res.values[0].close}`);
        }
      } catch(e) {}
    }
  } catch(e) {
    console.log('美股数据获取失败');
  }
}

async function main() {
  console.log(`${colors.yellow}📊 全球金融市场数据${colors.reset}`);
  console.log(new Date().toLocaleString('zh-CN'));
  
  await Promise.all([
    getCrypto(),
    getRMBRate(),
    getChinaStock(),
    getHKStock(),
    getUSStock()
  ]);
  
  console.log(`\n${colors.yellow}=== 数据来源 ===${colors.reset}`);
  console.log('加密货币: Binance API');
  console.log('汇率: ExchangeRate.host');
  console.log('A股: 新浪财经');
  console.log('港股/美股: Twelve Data (Demo)');
}

main().catch(console.error);
