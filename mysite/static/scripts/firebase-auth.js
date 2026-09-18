// Steam is the only login method wired up for now. It requires a manual
// step: Steam's OpenID realm for this game is locked to Lava Flame's own
// domain (legendsofidleon.com/steamsso/), not ours, so we can't read the
// popup's URL programmatically (browser same-origin policy) — the user has
// to copy it out and paste it back. This matches IdleonToolbox's own flow.

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-app.js";
import { getAuth, onAuthStateChanged, signInWithCustomToken, signOut } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-auth.js";
import { getFirestore, doc, getDoc } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-firestore.js";
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

// secondary data, don't block the save on it
async function readOr(read, fallback, label) {
    try {
        return (await read()) ?? fallback;
    } catch (e) {
        console.error(`${label} read failed (continuing without it):`, e);
        return fallback;
    }
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

let exchanging = false;

// one-time-use link, don't let a double-click spend it twice
async function exchangeSteamUrl(pastedUrl) {
    if (exchanging) return;
    exchanging = true;
    const submitButton = document.querySelector("#steam-login-submit");
    submitButton.disabled = true;

    try {
        await runSteamExchange(pastedUrl);
    } finally {
        exchanging = false;
        submitButton.disabled = false;
    }
}

function parseSteamUrl(pasted) {
    const withScheme = /^https?:\/\//i.test(pasted) ? pasted : `https://${pasted}`;
    try {
        const url = new URL(withScheme);
        const host = url.hostname.replace(/^www\./, "");
        return host === "legendsofidleon.com" && url.pathname.startsWith("/steamsso") ? url : null;
    } catch {
        return null;
    }
}

async function runSteamExchange(pastedUrl) {
    const url = parseSteamUrl(pastedUrl);
    if (!url) {
        showFriendlyError(
            `That doesn't look like the right page. The URL should start with <code>${STEAM_REALM}</code> — ` +
            `make sure you copied it from the tab Steam redirected you to, not the Steam login page itself.`
        );
        return;
    }

    const claimedId = url.searchParams.get("openid.claimed_id") || "";
    const steamParams = {
        claimedId: (claimedId.match(/\/(\d+)$/) || [])[1],
        nonce: url.searchParams.get("openid.response_nonce"),
        assocHandle: url.searchParams.get("openid.assoc_handle"),
        sig: url.searchParams.get("openid.sig"),
        signed: url.searchParams.get("openid.signed"),
    };

    let response, json;
    try {
        response = await fetch(ASIL_ENDPOINT, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ data: steamParams }),
        });
        json = await response.json().catch(() => null);
    } catch (e) {
        console.error("Steam token exchange failed:", e);
        showFriendlyError("Couldn't reach the login service. Please try again in a moment.");
        return;
    }

    const token = json?.result;
    if (!token || typeof token !== "string") {
        console.error("Steam token exchange returned no token:", response.status, json);
        showFriendlyError(response.status >= 500
            ? "The login service had a problem. Try again in a moment — if it keeps failing, " +
              "click \"Or log in with Steam\" again to get a fresh link."
            : "Couldn't log in with that link. Steam sign-in links only work once, so if this one was " +
              "already used, click \"Or log in with Steam\" again to get a fresh one."
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

    syncSteamSave(uid);
}

let syncing = false;

// one-shot load, only on login or Sync Steam
async function syncSteamSave(uid) {
    if (syncing) return;
    syncing = true;
    const syncButton = document.querySelector("#steam-sync");
    syncButton.disabled = true;

    try {
        let snap;
        try {
            snap = await getDoc(doc(firestore, "_data", uid));
        } catch (e) {
            console.error("Save read failed:", e);
            showFriendlyError("Couldn't load your save data. Please try again, or paste your save JSON manually below.");
            return;
        }
        if (!snap.exists()) {
            showFriendlyError(
                "No save data found for this account yet. Make sure you're logging in with " +
                "the account you actually play IdleOn with, and that you've played at least once."
            );
            return;
        }

        const [charNames, companion, serverVars] = await Promise.all([
            readOr(async () => (await get(child(ref(database), `_uid/${uid}`))).val(), [], "charNames"),
            readOr(async () => (await get(child(ref(database), `_comp/${uid}`))).val(), {}, "companion"),
            readOr(async () => (await getDoc(doc(firestore, "_vars", "_vars"))).data(), {}, "serverVars"),
        ]);

        document.querySelector("#player").value = JSON.stringify({ data: snap.data(), charNames, companion, serverVars });
        document.querySelector("#steam-login-wrapper").classList.remove("open");
        // Clicked from the open sidebar: full submit, spinner and sidebar
        // close included, same as a manual paste-and-submit.
        document.querySelector("form").requestSubmit();
    } finally {
        syncing = false;
        syncButton.disabled = false;
    }
}

async function signOutOfSteam() {
    try {
        await signOut(auth);
    } catch (e) {
        console.error("Sign-out failed:", e);
        showFriendlyError("Couldn't sign out. Please try again.");
    }
}

// both start hidden: nothing to click if firebase never loads
onAuthStateChanged(auth, (user) => {
    document.querySelector("#steam-login-open").hidden = !!user;
    document.querySelector("#steam-signed-in").hidden = !user;
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

    document.querySelector("#steam-sync").addEventListener("click", () => {
        if (auth.currentUser) syncSteamSave(auth.currentUser.uid);
    });

    document.querySelector("#steam-sign-out").addEventListener("click", signOutOfSteam);
}

document.addEventListener("DOMContentLoaded", initFirebaseLogin);
