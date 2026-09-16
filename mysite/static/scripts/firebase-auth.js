// Steam, Google and Apple all sign in to Lava's own Firebase project, since
// that's where the cloud save lives. None of them can use signInWithPopup:
// that enforces an authorised-domain list we're not on. Steam goes through
// Lava's asil function for a custom token; Google and Apple use device-code
// flows and end at signInWithCredential, which has no domain check. Steam
// additionally needs a manual copy-paste because its OpenID realm is locked
// to legendsofidleon.com. This matches IdleonToolbox's own flows.

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-app.js";
import {
    getAuth, onAuthStateChanged, signInWithCustomToken, signInWithCredential,
    GoogleAuthProvider, OAuthProvider, signOut
} from "https://www.gstatic.com/firebasejs/10.13.2/firebase-auth.js";
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

// Lava's own OAuth client, as used by the game client and IdleonToolbox
const GOOGLE_CLIENT_ID = "267901585099-u6fjd75v6k9gefq7bcokcndv99riir5j";
const GOOGLE_CLIENT_SECRET = "HzoZF-UKUNfFwBuz4vafwsaR";
const GOOGLE_DEVICE_ENDPOINT = "https://oauth2.googleapis.com/device/code";
const GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token";
const GOOGLE_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code";

// tspa/capsc send no CORS headers, so they go through our own proxy
const APPLE_START = "/apple-auth/start";
const APPLE_STATUS = "/apple-auth/status";
const APPLE_CLIENT_ID = "com.lavaflame.idleon.service.signin";
const APPLE_REDIRECT_URI = "https://us-central1-idlemmo.cloudfunctions.net/xapsi";

const POLL_TIMEOUT_MS = 15 * 60 * 1000;

const app = initializeApp(IDLEMMO_CONFIG);
const auth = getAuth(app);
const firestore = getFirestore(app);
const database = getDatabase(app);

function showFriendlyError(message) {
    // Reuses main.js's existing error modal rather than inventing new UI.
    // statusCode 0 is fine — it's only used for a console.log.
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

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const postForm = (url, params = {}) =>
    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(params),
    }).then((r) => r.json());

// Safari only allows window.open from inside the click handler itself, so the
// popup opens empty and is pointed at the provider once the device code arrives.
const openBlankPopup = () => window.open("", "_blank", "popup");

function sendPopupTo(popup, url) {
    if (popup && !popup.closed) popup.location.href = url;
    else window.open(url, "_blank", "popup");
}

function closePopup(popup) {
    if (popup && !popup.closed) popup.close();
}

// bumped to abandon an in-flight device poll when its panel closes
let devicePoll = 0;

function closeAllPanels() {
    devicePoll++;
    document.querySelectorAll("#steam-login-wrapper, #device-login-wrapper")
        .forEach((panel) => panel.classList.remove("open"));
}

// give up if the panel was dismissed or the user closed the provider's tab,
// rather than leaving the button disabled until the poll times out
function abandoned(mine, popup) {
    if (devicePoll !== mine) return true;
    if (popup && popup.closed) {
        closeAllPanels();
        return true;
    }
    return false;
}

/* ---------- Steam ---------- */

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

async function runSteamExchange(pastedUrl) {
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
              "click \"Log in with Steam\" again to get a fresh link."
            : "Couldn't log in with that link. Steam sign-in links only work once, so if this one was " +
              "already used, click \"Log in with Steam\" again to get a fresh one."
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

    syncSave(uid);
}

/* ---------- device-code panel ---------- */

// Google shows a code to type, Apple doesn't. Both get the link, since a
// popup blocker leaves it as the only way through.
function showDevicePanel(provider, { url, code, linkLabel } = {}) {
    document.querySelector("#device-login-provider").textContent = provider;

    const codeBox = document.querySelector("#device-login-code-box");
    codeBox.hidden = !code;
    if (code) document.querySelector("#device-login-code").textContent = code;

    const link = document.querySelector("#device-login-link");
    link.href = url;
    link.textContent = linkLabel || url.replace(/^https?:\/\//, "");

    document.querySelector("#device-login-wrapper").classList.add("open");
}

/* ---------- device flows ---------- */

let deviceLoginInFlight = false;

// one at a time: two concurrent polls can both resolve and race each other
// into signInWithCredential. The popup must open before the first await,
// while we're still inside the click handler, or Safari blocks it.
async function startDeviceLogin(provider, run) {
    if (deviceLoginInFlight) return;
    deviceLoginInFlight = true;
    const buttons = [...document.querySelectorAll("#signin-buttons button")];
    buttons.forEach((b) => (b.disabled = true));
    const popup = openBlankPopup();

    try {
        await run(popup);
    } catch (e) {
        closePopup(popup);
        closeAllPanels();
        console.error(`${provider} sign-in failed:`, e);
        showFriendlyError(`Couldn't reach ${provider}. Please check your connection and try again.`);
    } finally {
        deviceLoginInFlight = false;
        buttons.forEach((b) => (b.disabled = false));
    }
}

// Wait, check for abandonment, then let the provider decide: return a value to
// finish, giveUp to stop quietly, retryIn to change the gap, or nothing to wait
// again. Shared so the cancellation bookkeeping only exists once.
async function pollDevice({ popup, waitMs, deadline, timeoutMessage, tick }) {
    const mine = devicePoll;
    let wait = waitMs;

    while (Date.now() < deadline) {
        await sleep(wait);
        if (abandoned(mine, popup)) return null;

        const { value, giveUp, retryIn } = await tick(wait);
        if (value) return value;
        if (giveUp) return null;
        if (retryIn) wait = retryIn;
    }

    closeAllPanels();
    showFriendlyError(timeoutMessage);
    return null;
}

/* ---------- Google ---------- */

async function runGoogleLogin(popup) {
    const start = await postForm(GOOGLE_DEVICE_ENDPOINT, {
        client_id: GOOGLE_CLIENT_ID,
        scope: "email profile",
    });

    if (!start?.device_code || !start?.user_code) {
        closePopup(popup);
        console.error("Google device code request failed:", start);
        showFriendlyError("Couldn't start the Google sign-in. Please try again in a moment.");
        return;
    }

    const verifyUrl = start.verification_url || "https://www.google.com/device";
    sendPopupTo(popup, verifyUrl);
    showDevicePanel("Google", { url: verifyUrl, code: start.user_code });

    const idToken = await pollDevice({
        popup,
        waitMs: (start.interval || 5) * 1000,
        deadline: Date.now() + Math.min((start.expires_in || 900) * 1000, POLL_TIMEOUT_MS),
        timeoutMessage: "That sign-in code expired. Please try again.",
        tick: (wait) => googleTokenTick(start.device_code, wait),
    });
    if (!idToken) return;

    closePopup(popup);
    await finishCredentialLogin(GoogleAuthProvider.credential(idToken, null));
}

async function googleTokenTick(device_code, wait) {
    const result = await postForm(GOOGLE_TOKEN_ENDPOINT, {
        client_id: GOOGLE_CLIENT_ID,
        client_secret: GOOGLE_CLIENT_SECRET,
        device_code,
        grant_type: GOOGLE_GRANT_TYPE,
    }).catch(() => ({ error: "network" }));

    if (result?.id_token) return { value: result.id_token };
    // a dropped request shouldn't end a 15 minute window
    if (result?.error === "network" || result?.error === "authorization_pending") return {};
    if (result?.error === "slow_down") return { retryIn: wait + 5000 };

    closeAllPanels();
    console.error("Google device flow ended:", result);
    showFriendlyError(
        result?.error === "access_denied" ? "Google sign-in was cancelled."
            : result?.error === "expired_token" ? "That sign-in code expired. Please try again."
                : "Couldn't reach Google. Please check your connection and try again."
    );
    return { giveUp: true };
}

/* ---------- Apple ---------- */

async function runAppleLogin(popup) {
    const start = await postForm(APPLE_START);

    if (!start?.device_code || !start?.statusToken) {
        closePopup(popup);
        console.error("Apple device code request failed:", start);
        showFriendlyError("Couldn't start the Apple sign-in. Please try again in a moment.");
        return;
    }

    const params = new URLSearchParams({
        client_id: APPLE_CLIENT_ID,
        nonce: start.h_nonce,
        redirect_uri: APPLE_REDIRECT_URI,
        response_mode: "form_post",
        response_type: "code id_token",
        scope: "email",
        code: start.device_code,
        state: start.statusToken,
    });
    const authorizeUrl = `https://appleid.apple.com/auth/authorize?${params.toString()}`;
    sendPopupTo(popup, authorizeUrl);
    showDevicePanel("Apple", { url: authorizeUrl, linkLabel: "the Apple sign-in page" });

    // capsc reports nothing but success, so there's no error branch to read
    const credential = await pollDevice({
        popup,
        waitMs: 3000,
        deadline: Date.now() + POLL_TIMEOUT_MS,
        timeoutMessage: "The Apple sign-in timed out. Please try again.",
        tick: async () => {
            const result = await postForm(APPLE_STATUS, { device_code: start.device_code, statusToken: start.statusToken })
                .catch(() => null);
            return result?.id_token ? { value: result } : {};
        },
    });
    if (!credential) return;

    closePopup(popup);
    await finishCredentialLogin(
        new OAuthProvider("apple.com").credential({
            idToken: credential.id_token,
            rawNonce: credential.nonce,
        })
    );
}

/* ---------- shared ---------- */

async function finishCredentialLogin(credential) {
    let uid;
    try {
        const result = await signInWithCredential(auth, credential);
        uid = result.user.uid;
    } catch (e) {
        closeAllPanels();
        console.error("Firebase sign-in failed:", e);
        showFriendlyError(e?.code === "auth/account-exists-with-different-credential"
            ? "That email is already linked to a different sign-in method. Try the one you used originally."
            : "Couldn't complete the login. Please try again."
        );
        return;
    }
    syncSave(uid);
}

let syncing = false;

// one-shot load, only on login or Sync save
async function syncSave(uid) {
    if (syncing) return;
    syncing = true;
    const syncButton = document.querySelector("#cloud-sync");
    syncButton.disabled = true;
    closeAllPanels();  // sign-in is done, don't leave a panel behind an error

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
        // Clicked from the open sidebar: full submit, spinner and sidebar
        // close included, same as a manual paste-and-submit.
        document.querySelector("form").requestSubmit();
    } finally {
        syncing = false;
        syncButton.disabled = false;
    }
}

async function signOutOfCloud() {
    try {
        await signOut(auth);
    } catch (e) {
        console.error("Sign-out failed:", e);
        showFriendlyError("Couldn't sign out. Please try again.");
    }
}

// all start hidden: nothing to click if firebase never loads
onAuthStateChanged(auth, (user) => {
    document.querySelector("#signin-buttons").hidden = !!user;
    document.querySelector("#signed-in").hidden = !user;
});

function initFirebaseLogin() {
    document.querySelector("#steam-login-open").addEventListener("click", openSteamPopup);
    document.querySelector("#google-login-open")
        .addEventListener("click", () => startDeviceLogin("Google", runGoogleLogin));
    document.querySelector("#apple-login-open")
        .addEventListener("click", () => startDeviceLogin("Apple", runAppleLogin));

    // Same close-on-backdrop-click idiom as the existing settings panel
    // (main.js: setupSwitchBox) — clicking the overlay itself closes it,
    // clicking the panel content inside it does not.
    document.querySelectorAll("#steam-login-wrapper, #device-login-wrapper").forEach((wrapper) => {
        wrapper.addEventListener("click", (e) => {
            if (e.target === e.currentTarget) e.currentTarget.classList.remove("open");
        });
    });

    document.querySelector("#steam-login-submit").addEventListener("click", () => {
        exchangeSteamUrl(document.querySelector("#steam-login-url").value.trim());
    });

    document.querySelector("#steam-login-url").addEventListener("keydown", (e) => {
        if (e.key !== "Enter") return;
        e.preventDefault(); // don't let Enter submit the outer form with an empty #player
        exchangeSteamUrl(e.target.value.trim());
    });

    document.querySelector("#cloud-sync").addEventListener("click", () => {
        if (auth.currentUser) syncSave(auth.currentUser.uid);
    });

    document.querySelector("#sign-out").addEventListener("click", signOutOfCloud);
}

document.addEventListener("DOMContentLoaded", initFirebaseLogin);
