const opts = {
  lines: 13, // The number of lines to draw
  length: 38, // The length of each line
  width: 17, // The line thickness
  radius: 45, // The radius of the inner circle
  scale: 1, // Scales overall size of the spinner
  corners: 1, // Corner roundness (0..1)
  speed: 1, // Rounds per second
  rotate: 28, // The rotation offset
  animation: 'spinner-line-fade-default', // The CSS animation name for the lines
  direction: 1, // 1: clockwise, -1: counterclockwise
  color: '#ffffff', // CSS color or array of colors
  fadeColor: 'transparent', // CSS color or array of colors
  top: '50%', // Top position relative to parent
  left: '50%', // Left position relative to parent
  shadow: '0 0 1px transparent', // Box-shadow for the lines
  zIndex: 10, // The z-index (defaults to 2e9)
  className: 'spinner', // The CSS class to assign to the spinner
  position: 'absolute', // Element positioning
};

const defaults = {
    player: "",
    autoloot: "off",
    sheepie: "off",
    doot: "off",
    order_tiers: "off",
    progress_bars: "off",
    handedness: "off",
    light: "off"
}

const spinner = new Spin.Spinner(opts)

function toggleSidebar() {
    document.querySelectorAll('#drawer, #drawer-handle').forEach(e => e.classList.toggle('sidebar-open'))
}

// close the sidebar if clicked outside of it or not on hamburger
document.addEventListener("click", (e) => {
    let drawer = e.target.closest("#drawer") || e.target.closest("#drawer-handle")
    let sidebar = document.getElementById("drawer")
    if (!drawer && sidebar.classList.contains("sidebar-open")) {
        toggleSidebar()
    }
})

// close the sidebar if it's open and Esc key is pressed
document.addEventListener("keydown", (e) => {
    let escPressed = e.code === "Escape"
    if (escPressed) toggleSidebar()
})

function openSidebarIfFirstAccess() {
    // show sidebar if opening the page for the first time
    if (document.querySelectorAll('main, .error').length === 0) {
        toggleSidebar()
    }
}

function defineFormSubmitAction() {
    document.querySelector('form').addEventListener('submit', (e) => {
        e.preventDefault()

        const formData = new FormData(e.target)
        formData.set('light', localStorage.getItem('light'))
        storeUserParams(Object.fromEntries(formData))

        const target = document.querySelector("#top")
        target.innerHTML = ""
        spinner.spin(target)

        const data = fetchStoredUserParams()
        fetchPlayerAdvice(data)
        toggleSidebar()
    })
}

// calculate progress bars
function calcProgressBars(parent = document) {
    const top = el => el.getBoundingClientRect().top

    parent.querySelectorAll(".progress-box").forEach(progressBox => {
        const checkbox= document.querySelector('#progress_bars')
        const advice = progressBox.nextElementSibling
        const siblings = Array.from(advice.parentElement.children)
        const idx = siblings.indexOf(advice)
        const prog = siblings[idx + 1]
        const goal = siblings[idx + 3]
        const row = siblings.slice(idx, idx + 4)
        const rowWidth = row.reduce((total, curr) => total + curr.offsetWidth, 0)
        const [progCoefficient, show] = progWidth(progressBox, rowWidth, prog, goal)

        const rowHeight = advice.offsetHeight
        const rowTop = top(advice) - top(advice.parentElement) + advice.parentElement.scrollTop

        const progressBar = progressBox.querySelector(".progress-bar")
        progressBar.style.width = `${progCoefficient}%`

        progressBox.style.height = `${rowHeight}px`
        progressBox.style.top = `${rowTop}px`

        if (checkbox.value === "off" || !show) {
            progressBox.classList.add('hidden')
        } else if (show) {
            progressBox.classList.remove('hidden')
        }
    })
}

function progWidth(bar, w, p, g) {
    const toFloat = e => parseFloat(e.innerText.replace(/.*?([\d.]+).*/, "$1"))
    const goal = toFloat(g)
    const prog = toFloat(p)
    const inPercentages = g.innerText.includes("%") || p.innerText.includes("%")
    const inRatio = !(isNaN(prog) || isNaN(goal))
    const isDone = [g.innerText, p.innerText].some(el => el === "✔")


    if (inRatio)       return [(100 * Math.min(prog, goal) / goal), true]
    if (inPercentages) return [Math.min([prog, goal].find(e => !isNaN(e)), 100), true]
    if (isDone)        return [100, true]

    return [0, (inPercentages || inRatio)]
}

const hideProgressBoxes = (parent = document) => parent
    .querySelectorAll('.progress-box')
    .forEach(box => box.classList.add("hidden"))

let resizeTimer;
window.addEventListener('resize', () => {
    if (!resizeTimer) hideProgressBoxes()

    clearTimeout(resizeTimer);

    resizeTimer = setTimeout(() => {
        calcProgressBars()
        resizeTimer = null
    }, 100)
})

function setupFolding() {
    // set event listeners for folding worlds and sections
    document.querySelectorAll('.toggler').forEach(toggler => toggler.onclick = (e) => {
        let title = e.currentTarget
        for (const element of [title, title.nextElementSibling]) {
            element.classList.toggle("folded")
        }
    })
}

function setupLightSwitch() {
    document.querySelector('#light-switch').onclick = (e) => {
        document.documentElement.classList.toggle('light-mode')
        e.currentTarget.classList.toggle('on')
        e.currentTarget.classList.toggle('off')
        localStorage.setItem('light', e.currentTarget.classList[0])
    }
}

function setupSidebarToggling() {
    document.querySelector('#drawer-handle').onclick = toggleSidebar
}

function setupSubmitKeybind() {
    // submit the form content if the text area is focused and (Ctrl|Cmd) + Enter is pressed
    document.querySelector("textarea[name='player']").addEventListener("keypress", e => {
        let ctrlCmdPressed = e.ctrlKey || e.metaKey
        let enterPressed = e.code === "Enter"

        if (!(ctrlCmdPressed && enterPressed)) return

        let clickEvent = new MouseEvent('click', {
            'view': window,
            'bubbles': true,
            'cancelable': true
        });
        document.querySelector('input[type="submit"]').dispatchEvent(clickEvent);
    })
}

function setupColorScheme() {
    const runColorMode = (fn) => {
        if (!window.matchMedia) return
        const query = window.matchMedia('(prefers-color-scheme: light)')
        fn(query.matches)
        query.addEventListener('change', (event) => fn(event.matches))
    }

    const body = document.documentElement.classList
    const cls = 'light-mode'

    // Check localStorage for a saved theme preference
    const savedTheme = localStorage.getItem('light');

    if (savedTheme !== null) {
        // Apply the saved theme preference
        savedTheme === 'on' ? body.add(cls) : body.remove(cls)

        // Update the light switch element accordingly
        let lightSwitch = document.querySelector('#light-switch')
        lightSwitch.classList.add(savedTheme === 'on' ? 'on' : 'off');
    } else {
        // If no preference is saved in localStorage, use the system preference
        runColorMode((isLightMode) => {
            let lightSwitch = document.querySelector('#light-switch')
            isLightMode ? body.add(cls) : body.remove(cls)
            lightSwitch.classList.add(isLightMode ? 'on' : 'off')
        });
    }
}

function setupSwitchesActions() {
    // change colour and position of switches when clicked
    document.querySelectorAll('.slider').forEach(label => label.onclick = e => {
        const lbl = e.currentTarget
        const shaft = lbl.querySelector(".shaft")
        shaft.classList.toggle("on")
        shaft.classList.toggle("off")
        const checkbox = lbl.previousElementSibling
        checkbox.value = checkbox.value === "on" ? "off" : "on"

        localStorage.setItem(e.currentTarget.getAttribute("for"), checkbox.value)
    })

    // handle left/right handedness switching
    document.querySelector('#handedness').onclick = () => {
        document.querySelectorAll('.slider, .nav-links, #drawer-handle').forEach(s => s.classList.toggle('lefty'))
    }

    // toggle progress bars
    document.querySelector('#progress_bars').onclick = () => calcProgressBars(document)
}

function setupPinchyHrefActions() {
    document.querySelectorAll('#pinchy .advice-group a').forEach(hyperlink => hyperlink.onclick = e => {
        const link = e.currentTarget
        const targetId = link.getAttribute("href").slice(1)
        const target = document.querySelector(`#${targetId}`)
        target.parentElement.classList.remove('folded')
        target.querySelectorAll('*:not(.empty)').forEach(c => c.classList.remove('folded'))
    })
}

function applyShowMoreButton() {
    const expandableSections = document.querySelectorAll("#gem-shop .advice-section, #greenstacks .advice-section, #cards .advice-section")
    expandableSections.forEach(section => {
        const expandableGroups = section.querySelector(".groups")
        const showMoreButton = section.querySelector(".show-more")
        const groups = Array.from(expandableGroups.querySelectorAll(".advice-group.hidden"))

        showMoreButton.style.display = (groups.length > 0) ? "block" : "none"

        showMoreButton.onclick = e => {
            const button = e.currentTarget

            const group = groups.shift()
            group.classList.remove("hidden")
            calcProgressBars(group)
            if (groups.length === 0) {
                button.style.display = "none"
            }
        }
    })
}

function setupToggleAllAction() {
    document.querySelector("#expand-collapse").onclick = e => {
        const button = e.currentTarget
        button.classList.toggle("closed")
        document.querySelectorAll('.toggler').forEach(e => {
            let title = e
            for (const element of [title, title.nextElementSibling]) {
                button.classList.contains("closed") ? element.classList.add("folded") : element.classList.remove("folded")
            }
        })
    }
}

let clockTick
function setupDataClock() {
    clearInterval(clockTick)
    clockTick = setInterval(() => {
        const elapsed = document.querySelector('#elapsed')
        const timeStr = elapsed.innerText
        const [sec, min, hr, d] = timeStr.split(":").reverse()
        let _sec = parseInt(sec) + 1
        let _min = Math.floor(_sec / 60)
        _sec = _sec % 60

        _min = parseInt(min) + _min
        let _hr = Math.floor(_min / 60)
        _min = _min % 60

        _hr = parseInt(hr) + _hr
        let _d = Math.floor(_hr / 60)
        _hr = _hr % 60

        _d = parseInt(d) + _d
        elapsed.innerText = [
            _d.toString().padStart(2, "0"),
            _hr.toString().padStart(2, "0"),
            _min.toString().padStart(2, "0"),
            _sec.toString().padStart(2, "0")
        ].join(":")
    }, 1000)
}

function setFormValues() {
    const form = document.querySelector('form')
    const userParams = fetchStoredUserParams()

    Object.entries(defaults).forEach(([k, v]) => {
        const userValue = userParams[k] || v
        const input = form.querySelector(`[name=${k}]`)
        if (k === "player")
            input.innerText = userValue
        else if (input.value.toString() !== userValue)
            form.querySelector(`[for=${k}]`).click()
    })
}

function loadResults(html) {
    spinner.stop()
    const mainWrapper = document.getElementById('top');
    mainWrapper.innerHTML = html;
}

function fetchPlayerAdvice(currentParams) {
    initBaseUI(currentParams)

    fetch("/results", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(currentParams)

    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.text();

    }).then(html => {
        if (html === "") {
            openSidebarIfFirstAccess()
            return
        }
        loadResults(html);
        initResultsUI()

    }).catch(error => {
        console.error('Error:', error);
    });
}

const storeUserParams = (data) => Object
    .entries(defaults)
    .forEach(([k, v]) => localStorage.setItem(k, data[k] || v))

const fetchStoredUserParams = () => Object.fromEntries(Object.entries(defaults)
    .map(([k, v]) => [k, localStorage.getItem(k) || v]))

function storeGetParamsIfProvided() {
    const GETData = new URLSearchParams(window.location.search).entries();
    const truthy = [true, "True", "true", "on"]
    const falsy = [false, "False", "false", "off"]
    GETData.forEach(([k, v]) => localStorage.setItem(k, truthy.includes(v) ? "on" : falsy.includes(v) ? "off" : v))
}

document.addEventListener("DOMContentLoaded", () => {
    storeGetParamsIfProvided()
    fetchPlayerAdvice(fetchStoredUserParams())
})

function hideSpinnerIfFirstAccess() {
    if (! localStorage.getItem('player'))
        return
    var target= document.querySelector('#top');
    spinner.spin(target);
}

function defineCookieModalAction() {
    if (document.cookie.includes("EU_COOKIE_LAW_CONSENT=true")) return

    const modal = document.querySelector('#cookie-policy');
    const openModalBtn = document.querySelector('.eupopup-button_2');
    const closeModalSpan = document.querySelector('#close-modal');

    openModalBtn.setAttribute("href", "")

    openModalBtn.onclick = (e) => {
        e.preventDefault()
        modal.classList.add('show');
    }

    closeModalSpan.onclick = () => {
        modal.classList.remove('show');
    }

    window.onclick = (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
        }
    }
}

function initBaseUI(storageParams) {
    setTimeout(defineCookieModalAction, 1000)
    hideSpinnerIfFirstAccess(storageParams)
    defineFormSubmitAction()
    setupLightSwitch()
    setupSidebarToggling()
    setupSubmitKeybind()
    setupColorScheme()
    setupToggleAllAction()
    setupSwitchesActions()
}

function initResultsUI() {
    setFormValues()
    setupFolding()
    setupPinchyHrefActions()
    applyShowMoreButton()
    setupDataClock()
    calcProgressBars(document)
}
