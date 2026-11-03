// Bundled locally with esbuild. Only client SDKs; never include Admin SDK credentials.
export { initializeApp } from 'firebase/app';
export { getAuth, onAuthStateChanged, signInWithPopup, signInWithCredential,
  GoogleAuthProvider, OAuthProvider, signInWithRedirect, getRedirectResult, signOut, setPersistence, browserLocalPersistence,
  inMemoryPersistence, connectAuthEmulator, signInWithEmailAndPassword } from 'firebase/auth';
// Real-time listeners are required for mobile/desktop sync on Enterprise Native Mode.
// SQLite holds pending changes; no shared Firestore disk cache across accounts.
export { initializeFirestore, getFirestore, disableNetwork, enableNetwork, memoryLocalCache, collection, doc, onSnapshot,
  runTransaction, getDocFromServer, serverTimestamp, connectFirestoreEmulator } from 'firebase/firestore';
export { getStorage, ref, uploadBytes, getDownloadURL, connectStorageEmulator } from 'firebase/storage';
