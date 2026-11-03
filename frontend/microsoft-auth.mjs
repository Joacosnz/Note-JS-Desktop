// Complete Firebase's OAuth flow in the environment that owns the desktop session.
// Microsoft tokens are never replayed through the Google browser handoff.
export async function signInMicrosoft(sdk, auth, nativeDesktop) {
  const provider = new sdk.OAuthProvider('microsoft.com');
  provider.setCustomParameters({prompt:'select_account', tenant:'common'});
  return nativeDesktop
    ? sdk.signInWithRedirect(auth, provider)
    : sdk.signInWithPopup(auth, provider);
}

export function microsoftAuthMessage(error) {
  const messages = {
    'auth/account-exists-with-different-credential':'Esta dirección ya usa otro método de acceso. Iniciá sesión con el método original para acceder a esa cuenta.',
    'auth/operation-not-allowed':'Este método de acceso no está habilitado en Firebase Authentication.',
    'auth/invalid-oauth-client-id':'La configuración del proveedor en Firebase necesita revisar su identificador de cliente.',
    'auth/network-request-failed':'No se pudo conectar. Revisá tu conexión e intentá de nuevo.',
    'auth/popup-blocked':'Permití la ventana de Microsoft y volvé a intentarlo.',
    'auth/popup-closed-by-user':'Inicio de sesión cancelado.',
    'auth/cancelled-popup-request':'Inicio de sesión cancelado.'
  };
  return messages[error?.code] || null;
}
