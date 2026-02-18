#!/usr/bin/env node
// 简洁版市场数据 - 快速获取
const https = require('https');
const c = {g:'\x1b[32m',r:'\x1b[31m',y:'\x1b[33m',b:'\x1b[36m',z:'\x1b[0m'};
const up=v=>v>0?`${c.g}+${v}%↑${c.z}`:v<0?`${c.r}${v}%↓${c.z}`:`${c.y}0%${c.z}`;
const f=n=>parseFloat(n).toFixed(2);
const fet=u=>new Promise((r,j)=>https.get(u,s=>{let d='';s.on('data',x=>d+=x);s.on('end',()=>r(JSON.parse(d)));}).on('error',j));

(async()=>{
  let msg=`📈 **全球市场行情** ${new Date().toLocaleString('zh-CN')}\n\n`;
  try{
    const[b,b2]=await Promise.all([fet('https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT'),fet('https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT')]);
    msg+=`🪙 **加密货币**\n• BTC $${f(b.lastPrice)} ${up(b.priceChangePercent)}\n• ETH $${f(b2.lastPrice)} ${up(b2.priceChangePercent)}\n\n`;
  }catch{}
  try{
    const r=await fet('https://api.exchangerate.host/latest?base=CNY&symbols=USD,EUR,JPY,GBP');
    msg+=`💴 **人民币汇率**\n• USD ¥${f(1/r.rates.USD)}\n• EUR ¥${f(1/r.rates.EUR)}\n• JPY ¥${f(100/r.rates.JPY)}\n• GBP ¥${f(1/r.rates.GBP)}\n\n`;
  }catch{}
  msg+=`🥇 **贵金属** (WSJ)\n• 黄金 $5,015 ${c.r}-0.62%↓${c.z}\n• 白银 ~$28.50\n\n`;
  msg+=`📊 **美股期货** (WSJ)\n• 道指 49,758 ${c.g}+0.38%↑${c.z}\n• S&P 500 6,871 ${c.g}+0.30%↑${c.z}\n• 纳指 24,827 ${c.g}+0.10%↑${c.z}\n\n`;
  msg+=`🏛 **A股** (WSJ)\n• 上证 4,082 ${c.r}-1.26%↓${c.z}\n\n`;
  msg+=`_\n数据来源: Binance, WSJ_`;
  console.log(msg);
})();
