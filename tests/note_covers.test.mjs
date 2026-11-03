import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {NOTE_COVERS,coverCss,desktopCoverToRemote,remoteCoverToDesktop,isLocalPhotoCover} from '../frontend/note-cover-contract.mjs';
test('all desktop gradient presets map to stable Android IDs and round trip',()=>{
  for(const preset of NOTE_COVERS){
    const remote=desktopCoverToRemote({hasCover:true,coverStyle:coverCss(preset),coverPositionY:73});
    assert.deepEqual(remote,{hasCover:true,coverPresetId:preset.id,coverPositionY:73});
    assert.equal(remoteCoverToDesktop(remote).coverStyle,coverCss(preset));
  }
});
test('changing a desktop cover takes precedence over its previously synced ID',()=>assert.equal(desktopCoverToRemote({hasCover:true,coverPresetId:'rose',coverStyle:coverCss(NOTE_COVERS[2])}).coverPresetId,'forest'));
test('old notes retain local covers; removal and numeric limits are explicit',()=>{
  assert.equal(remoteCoverToDesktop({}, {hasCover:true,coverStyle:'old-local-style'}).hasCover,true);
  assert.equal(remoteCoverToDesktop({hasCover:false,coverPresetId:'rose'}).hasCover,false);
  assert.equal(desktopCoverToRemote({}).coverPositionY,50);
  assert.equal(desktopCoverToRemote({coverPositionY:120}).coverPositionY,100);
  assert.equal(remoteCoverToDesktop({hasCover:true,coverPresetId:'url(unsafe)',coverPositionY:-5},null).coverStyle,coverCss(NOTE_COVERS[0]));
  assert.equal(remoteCoverToDesktop({hasCover:true,coverPositionY:NaN}).coverPositionY,50);
});
test('the desktop cover picker uses the shared palette',()=>{
  const app=fs.readFileSync(new URL('../frontend/app.js',import.meta.url),'utf8');
  const palette=app.match(/const COVER_PRESETS = \[([\s\S]*?)\];/)[1];
  const values=[...palette.matchAll(/'([^']+)'/g)].map(match=>match[1]);
  assert.deepEqual(values,NOTE_COVERS.map(coverCss));
});

test('cloud text updates preserve a local photograph without publishing its device URL',()=>{
  const style='url(/api/covers/'+'a'.repeat(64)+'.jpg)';
  assert.ok(isLocalPhotoCover(style));
  assert.equal(isLocalPhotoCover('url(/api/covers/../notejs.db)'),false);
  assert.equal(isLocalPhotoCover('url(https://example.com/photo.jpg)'),false);
  const local={hasCover:true,coverStyle:style};
  assert.equal(remoteCoverToDesktop({hasCover:true,coverPresetId:'forest'},local).coverStyle,style);
  assert.equal(remoteCoverToDesktop({hasCover:false},local).hasCover,false);
  assert.ok(!JSON.stringify(desktopCoverToRemote(local)).includes('/api/covers/'));
});
