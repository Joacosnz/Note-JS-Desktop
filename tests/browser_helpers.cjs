const {spawn} = require('node:child_process');
const fs = require('node:fs'),path = require('node:path');
const {once} = require('node:events');
const delay = ms => new Promise(resolve=>setTimeout(resolve,ms));
async function until(callback,message,timeout=30000) {
  const end=Date.now()+timeout;
  while(Date.now()<end){if(await callback())return;await delay(100);}
  throw new Error(message);
}
async function openBrowser(temporary) {
  const edge=process.env.NOTEJS_TEST_BROWSER || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
  const browserProcess=spawn(edge,['--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0',`--user-data-dir=${path.join(temporary,'edge')}`,'about:blank'],{windowsHide:true,stdio:'ignore'});
  const active=path.join(temporary,'edge','DevToolsActivePort');
  await until(()=>fs.existsSync(active),'Browser did not start');
  const port=fs.readFileSync(active,'utf8').split('\n')[0];
  const version=await fetch(`http://127.0.0.1:${port}/json/version`).then(r=>r.json());
  const socket=new WebSocket(version.webSocketDebuggerUrl);await once(socket,'open');
  let id=0;const pending=new Map();
  socket.onmessage=event=>{const data=JSON.parse(event.data);if(data.id&&pending.has(data.id)){const task=pending.get(data.id);pending.delete(data.id);data.error?task.reject(new Error(data.error.message)):task.resolve(data.result);}};
  const call=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const current=++id;pending.set(current,{resolve,reject});socket.send(JSON.stringify({id:current,method,params,...(sessionId?{sessionId}:{})}));});
  const {targetId}=await call('Target.createTarget',{url:'about:blank'});
  const {sessionId}=await call('Target.attachToTarget',{targetId,flatten:true});
  await call('Page.enable',{},sessionId);
  await call('Emulation.setDeviceMetricsOverride',{width:1360,height:900,deviceScaleFactor:1,mobile:false},sessionId);
  const evaluate=async expression=>{const data=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true},sessionId);if(data.exceptionDetails)throw new Error(data.exceptionDetails.exception?.description || data.exceptionDetails.text);return data.result.value;};
  return {evaluate,call,sessionId,navigate:url=>call('Page.navigate',{url},sessionId),close:async()=>{try{await call('Browser.close');}catch{}socket.close();browserProcess.kill();}};
}
module.exports={openBrowser,until,delay};
