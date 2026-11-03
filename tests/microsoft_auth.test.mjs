import {test} from 'node:test';
import assert from 'node:assert/strict';
import {signInMicrosoft,microsoftAuthMessage} from '../frontend/microsoft-auth.mjs';

function fixture() {
  const calls=[];
  class OAuthProvider {
    constructor(id) { this.providerId=id; }
    setCustomParameters(parameters) { this.parameters=parameters; }
  }
  const sdk={OAuthProvider,
    signInWithRedirect:async(auth,provider)=>{calls.push({method:'redirect',auth,provider});},
    signInWithPopup:async(auth,provider)=>{calls.push({method:'popup',auth,provider}); return {user:{uid:'microsoft-user'}};}
  };
  return {sdk,calls};
}
test('desktop Microsoft sign-in completes the Firebase redirect flow in the current session',async()=>{
  const {sdk,calls}=fixture(), auth={name:'desktop-session'};
  await signInMicrosoft(sdk,auth,true);
  assert.equal(calls.length,1);
  assert.equal(calls[0].method,'redirect');
  assert.equal(calls[0].auth,auth);
  assert.equal(calls[0].provider.providerId,'microsoft.com');
  assert.deepEqual(calls[0].provider.parameters,{prompt:'select_account',tenant:'common'});
});
test('browser Microsoft sign-in uses a popup and the same Firebase auth instance',async()=>{
  const {sdk,calls}=fixture(), auth={name:'browser-session'};
  const result=await signInMicrosoft(sdk,auth,false);
  assert.equal(calls[0].method,'popup');
  assert.equal(calls[0].auth,auth);
  assert.equal(result.user.uid,'microsoft-user');
});
test('provider collisions and blocked popups have actionable messages',()=>{
  assert.match(microsoftAuthMessage({code:'auth/account-exists-with-different-credential'}),/método original/);
  assert.match(microsoftAuthMessage({code:'auth/popup-blocked'}),/ventana/);
  assert.equal(microsoftAuthMessage({code:'unknown'}),null);
});
