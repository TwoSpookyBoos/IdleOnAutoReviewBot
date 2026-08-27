// Steam is the only login method wired up for now. It requires a manual
// step: Steam's OpenID realm for this game is locked to Lava Flame's own
// domain (legendsofidleon.com/steamsso/), not ours, so we can't read the
// popup's URL programmatically (browser same-origin policy) — the user has
// to copy it out and paste it back. This matches IdleonToolbox's own flow.

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-app.js";
import { getAuth, onAuthStateChanged, signInWithCustomToken } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-auth.js";
import { getFirestore, doc, onSnapshot } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-firestore.js";
import { getDatabase, ref, get, child } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-database.js";

const IDLEMMO_CONFIG = {
    apiKey: "AIzaSyAU62kOE6xhSrFqoXQPv6_WHxYilmoUxDk",
    authDomain: "idlemmo.firebaseapp.com",
    databaseURL: "idlemmo.firebaseio.com",
    storageBucket: "idlemmo.appspot.com",
    projectId: "idlemmo",
};
const STEAM_REALM = "https://www.legendsofidleon.com/steamsso/";
const ASIL_ENDPOINT = "https://us-central1-idlemmo.cloudfunctions.net/asil";

const app = initializeApp(IDLEMMO_CONFIG);
const auth = getAuth(app);
const firestore = getFirestore(app);
const database = getDatabase(app);

function showFriendlyError(message) {
    // Reuses main.js's existing error modal (main.js:384) rather than
    // inventing new UI. statusCode 0 is fine — it's only used for a console.log.
    window.loadErrorPopup(message, 0);
}

function openSteamPopup() {
    const params = new URLSearchParams({
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.return_to": STEAM_REALM,
        "openid.realm": STEAM_REALM,
        "openid.mode": "checkid_setup",
    });
    window.open(`https://steamcommunity.com/openid/login?${params.toString()}`, "_blank", "popup");
    document.querySelector("#steam-login-wrapper").classList.add("open");
    document.querySelector("#steam-login-url").focus();
}

async function exchangeSteamUrl(pastedUrl) {
    if (!pastedUrl.startsWith(STEAM_REALM)) {
        showFriendlyError(
            `That doesn't look like the right page. The URL should start with <code>${STEAM_REALM}</code> — ` +
            `make sure you copied it from the tab Steam redirected you to, not the Steam login page itself.`
        );
        return;
    }

    let steamParams;
    try {
        const url = new URL(pastedUrl);
        const claimedId = url.searchParams.get("openid.claimed_id") || "";
        steamParams = {
            claimedId: (claimedId.match(/\/(\d+)$/) || [])[1],
            nonce: url.searchParams.get("openid.response_nonce"),
            assocHandle: url.searchParams.get("openid.assoc_handle"),
            sig: url.searchParams.get("openid.sig"),
            signed: url.searchParams.get("openid.signed"),
        };
    } catch {
        showFriendlyError("Couldn't read that as a URL — make sure the whole address bar contents got pasted in.");
        return;
    }

    let token;
    try {
        const response = await fetch(ASIL_ENDPOINT, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ data: steamParams }),
        });
        const json = await response.json();
        token = json?.result;
    } catch (e) {
        console.error("Steam token exchange failed:", e);
        showFriendlyError("Couldn't reach the login service. Please try again in a moment.");
        return;
    }

    if (!token || typeof token !== "string") {
        showFriendlyError(
            "Couldn't log in with that link. Steam sign-ins can only be completed once — " +
            "click \"Log in with Steam\" again to get a fresh one."
        );
        return;
    }

    let uid;
    try {
        const cred = await signInWithCustomToken(auth, token);
        uid = cred.user.uid;
    } catch (e) {
        console.error("Firebase sign-in failed:", e);
        showFriendlyError("Couldn't complete the login. Please try again.");
        return;
    }

    // Called directly rather than relying on onAuthStateChanged: that
    // listener (below) is one-shot and already fired once — with null —
    // before this login even started, so it won't fire again for this
    // sign-in. It only ever covers the "already had a persisted session at
    // page-load" case.
    watchSaveFor(uid);
}

// Tracks the live listener so re-logging in (e.g. a different Steam account)
// tears down the previous subscription instead of leaving it running.
let unsubscribeFromSave = null;

function watchSaveFor(uid) {
    if (unsubscribeFromSave) unsubscribeFromSave();

    let isFirstUpdate = true;
    unsubscribeFromSave = onSnapshot(
        doc(firestore, "_data", uid),
        async (snap) => {
            if (!snap.exists()) {
                if (isFirstUpdate) {
                    showFriendlyError(
                        "No save data found for this account yet. Make sure you're logging in with " +
                        "the account you actually play IdleOn with, and that you've played at least once."
                    );
                }
                isFirstUpdate = false;
                return;
            }
            const cloudsave = snap.data();

            // charNames/companion are supporting data — default gracefully
            // rather than blocking the primary save data on a secondary read failing.
            let charNames = [];
            try {
                const charNamesSnap = await get(child(ref(database), `_uid/${uid}`));
                charNames = charNamesSnap.val() ?? [];
            } catch (e) {
                console.error("charNames read failed (continuing without it):", e);
            }

            let companion = {};
            try {
                const companionSnap = await get(child(ref(database), `_comp/${uid}`));
                companion = companionSnap.val() ?? {};
            } catch (e) {
                console.error("companion read failed (continuing without it):", e);
            }

            const assembled = { data: cloudsave, charNames, companion };
            document.querySelector("#player").value = JSON.stringify(assembled);
            localStorage.setItem("player", JSON.stringify(assembled));

            if (isFirstUpdate) {
                isFirstUpdate = false;
                document.querySelector("#steam-login-wrapper").classList.remove("open");
                // First result this page-view: full submit, spinner and sidebar
                // close included, same as a manual paste-and-submit.
                document.querySelector("form").requestSubmit();
            } else {
                // A later cloud-save came in (auto-save or a manual in-game
                // save) while the user is already looking at their results —
                // refresh quietly, without wiping #top or toggling the sidebar.
                window.fetchPlayerAdvice();
            }
        },
        (e) => {
            console.error("Live save listener error:", e);
            showFriendlyError("Lost the connection to your save data. You can still paste your save JSON manually below.");
        }
    );
}

// Exposed so main.js's own on-load auto-submit (which replays whatever's
// cached in localStorage) can skip itself when a fresher live fetch is about
// to run instead — see fetchPlayerAdviceUnlessFirebaseWillHandleIt in main.js.
window.firebaseAuthReady = new Promise((resolve) => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
        unsubscribe();
        resolve(user);
    });
});
window.firebaseAuthReady.then((user) => {
    if (user) watchSaveFor(user.uid);
});

function initFirebaseLogin() {
    document.querySelector("#steam-login-open").addEventListener("click", openSteamPopup);

    // Same close-on-backdrop-click idiom as the existing settings panel
    // (main.js: setupSwitchBox) — clicking the overlay itself closes it,
    // clicking the panel content inside it does not.
    document.querySelector("#steam-login-wrapper").addEventListener("click", (e) => {
        e.target.classList.remove("open");
    });

    document.querySelector("#steam-login-submit").addEventListener("click", () => {
        exchangeSteamUrl(document.querySelector("#steam-login-url").value.trim());
    });

    document.querySelector("#steam-login-url").addEventListener("keydown", (e) => {
        if (e.key !== "Enter") return;
        e.preventDefault(); // don't let Enter submit the outer form with an empty #player
        exchangeSteamUrl(e.target.value.trim());
    });
}

document.addEventListener("DOMContentLoaded", initFirebaseLogin);
