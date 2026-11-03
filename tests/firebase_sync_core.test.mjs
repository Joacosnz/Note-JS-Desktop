import {test} from 'node:test';
import assert from 'node:assert/strict';
import {canonical,localSignature,hasLocalChanges,remoteRevision,writeDecision,newLocalId,compareRemoteUpdates} from '../frontend/firebase-sync-core.mjs';
const remote = {updatedAt:{seconds:100,nanoseconds:20}};
const note = () => ({id:1,title:'Hola',content:'<p>Texto</p>',updatedAt:100,cloud:{uid:'alice',remoteId:'r1',baseRevision:remoteRevision(remote)}});
test('signatures are deterministic and ignore sync metadata',()=>{
  assert.equal(canonical({b:2,a:1}),canonical({a:1,b:2}));
  const local=note(), signature=localSignature(local); local.cloud.remote={new:'metadata'};local.updatedAt++;
  assert.equal(localSignature(local),signature);
  local.content='Cambió';assert.notEqual(localSignature(local),signature);
});
test('never write another account library',()=>assert.equal(writeDecision(note(),'bob',remote),'wrong-account'));
test('unchanged local note does not overwrite remote',()=>{const local=note();local.cloud.syncedSignature=localSignature(local);assert.equal(hasLocalChanges(local),false);assert.equal(writeDecision(local,'alice',{updatedAt:222}),'unchanged');});
test('changed local note updates only the revision it read',()=>assert.equal(writeDecision(note(),'alice',remote),'update'));
test('concurrent mobile edit and first-link collision preserve both',()=>{
  assert.equal(writeDecision(note(),'alice',{updatedAt:{seconds:100,nanoseconds:21}}),'conflict');
  const local=note();local.cloud.baseRevision=null;assert.equal(writeDecision(local,'alice',remote),'conflict');
});
test('remote deletion does not resurrect a deleted note',()=>assert.equal(writeDecision(note(),'alice',null),'deleted-remotely'));
test('new local notes create a remote document',()=>{const local=note();local.cloud.baseRevision=null;assert.equal(writeDecision(local,'alice',null),'create');});
test('new local IDs cannot collide with timestamps already used',()=>assert.equal(newLocalId([{id:100},{id:101}],100),102));
test('older queued snapshots cannot replace a newer acknowledged revision',()=>{
  assert.equal(compareRemoteUpdates({updatedAt:{seconds:100,nanoseconds:10}},{updatedAt:{seconds:100,nanoseconds:20}}),-1);
  assert.equal(compareRemoteUpdates({updatedAt:1000},{updatedAt:{seconds:1,nanoseconds:0}}),0);
  assert.equal(compareRemoteUpdates({updatedAt:{seconds:2,nanoseconds:0}},{updatedAt:1000}),1);
  assert.equal(compareRemoteUpdates({},remote),null);
});
