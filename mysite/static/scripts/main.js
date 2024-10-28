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
    doot: "off",
    riftslug: "off",
    sheepie: "off",
    order_tiers: "off",
    hide_completed: "off",
    hide_informational: "off",
    hide_unrated: "off",
    progress_bars: "off",
    handedness: "off",
    light: "off"
}

const spinner = new Spin.Spinner(opts)

function toggleSidebar() {
    document.querySelectorAll('#drawer, #drawer-handle').forEach(e => e.classList.toggle('sidebar-open'))
}

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

        fetchPlayerAdvice()
        toggleSidebar()
    })
}

// calculate progress bars
function calcProgressBars(parent = document) {
    const top = el => el.getBoundingClientRect().top

    parent.querySelectorAll(".progress-box").forEach(progressBox => {
        const checkbox = document.querySelector('#progress_bars')
        const advice = progressBox.nextElementSibling
        const siblings = Array.from(advice.parentElement.children)
        const idx = siblings.indexOf(advice)
        const prog = siblings[idx + 2]
        const goal = siblings[idx + 4]
        const row = siblings.slice(idx, idx + 5)
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


    if (inRatio) return [(100 * Math.min(prog, goal) / goal), true]
    if (inPercentages) return [Math.min([prog, goal].find(e => !isNaN(e)), 100), true]
    if (isDone) return [100, true]

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

    // close the sidebar if clicked outside of it or not on hamburger
    document.addEventListener("click", (e) => {
        let drawer = e.target.closest("#drawer") || e.target.closest("#drawer-handle") || e.target.id === "close-modal-error"
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

function setTextareaDefaultFocusAction() {
    document.querySelector("#player").onclick = e => {
        e.currentTarget.focus()
        e.currentTarget.select()
    }
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

    // On Click Listener for the Hide Completed switch
    document.querySelector('label[for="hide_completed"]').addEventListener('click', hideComposite)

    // On Click Listener for the Hide Info switch
    document.querySelector('label[for="hide_informational"]').addEventListener('click', hideComposite)

    // On Click Listener for the Hide Info switch
    document.querySelector('label[for="hide_unrated"]').addEventListener('click', hideComposite)
}

function setupHrefEventActions() {
    addEventListener("hashchange", evt => {
        var h = location.hash.slice(1) || "pinchy-all" // Defaults on the pinchy section if you try to access an empty hash, for exemple when hiting return on your browser
        var target = (document.getElementById(h) || document.getElementsByName(h)[0] || document.body)
        unfoldElementIfFolded(target)
    });

    document.querySelectorAll('#mainresults .advice a').forEach(hyperlink => hyperlink.onclick = e => {
        const link = e.currentTarget
        const targetId = link.getAttribute("href").slice(1)

        // Delegate the navigation to the HashChange event
        e.preventDefault()
        history.pushState(undefined, undefined, `#${targetId}`);
        window.dispatchEvent(new HashChangeEvent("hashchange"))
    })
}

/**
 * Unfolds the section it is folded
 * @param {Element} target 
 */
function unfoldElementIfFolded(target) {
    var [sectionH1, sectionDiv] = findSectionElements(target)
    var [articleH1, articleDiv] = findArticlesElements(target);
    var articleElement = articleDiv?.parentElement;

    if (articleDiv?.classList.contains('folded')) {
        // The section is folded, we need to wait until the transition is complete to scroll to its position
        const onTransitionEnd = evt => { 
            if (evt.target == articleDiv) { // Multiple events are triggered, we only want the article div one
                articleElement.removeEventListener("transitionend", onTransitionEnd);
                target.scrollIntoView({behavior: "smooth"})
            }
        }
        articleElement.addEventListener("transitionend", onTransitionEnd)
    } else {
        // The section is open, scroll directly to it
        target.scrollIntoView({behavior: "smooth"})
    }

    articleH1?.classList.remove('folded');
    articleDiv?.classList.remove('folded');
    sectionH1?.classList.remove('folded');
    sectionDiv?.classList.remove('folded');
}

function findArticlesElements(target) {
    var div = target.closest('div.collapse-wrapper:has(> div.sections)') || document.querySelector('div.collapse-wrapper:has(> div.sections)');
    var h1 = div.parentElement.querySelector('h1.banner.toggler');
    return [h1, div]
}

function findSectionElements(target) {
    var div = target.closest('div.collapse-wrapper:has(> ul.advice-section)') || target.querySelector('div.collapse-wrapper:has(> ul.advice-section)');
    var h1 = div.parentElement.querySelector('h1.subheading.toggler')
    return [h1, div]
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
        document.querySelectorAll('.toggler').forEach(title => {
            for (const element of [title, title.nextElementSibling]) {
                button.classList.contains("closed") ? element.classList.add("folded") : element.classList.remove("folded")
            }
        })
    }
}

let clockTick

function setupDataClock() {
    clearInterval(clockTick);

    clockTick = setInterval(() => {
        const elapsed = document.querySelector('#elapsed')
        if (!elapsed) return

        const timeUnits = elapsed.innerText.split(":").reverse().map(n => parseInt(n))
        let carry = 1 // Initial increment of one second

        // Increment time units
        timeUnits.forEach((unit, index) => {
            if (carry <= 0) return
            const newUnit = unit + carry
            carry = Math.floor(newUnit / 60)
            timeUnits[index] = newUnit % 60
        })

        // Pad each unit and format the elapsed time string
        elapsed.innerText = timeUnits.map(unit => unit.toString().padStart(2, "0")).reverse().join(":")
    }, 1000)
}


function setFormValues() {
    const form = document.querySelector('form')
    const userParams = fetchStoredUserParams()

    Object.entries(defaults).forEach(([k, v]) => {
        const userValue = userParams[k] || v
        const input = form.querySelector(`[name=${k}]`)
        if (k === "player")
            input.value = userValue
        else if (input && input.value.toString() !== userValue)
            form.querySelector(`[for=${k}]`).click()
    })
}

function loadResults(html) {
    spinner.stop()
    const mainWrapper = document.getElementById('top');
    mainWrapper.innerHTML = html;

    initLazyLoading();
}

function initLazyLoading() {
    const images = document.querySelectorAll(".lazy");
    const observer = new IntersectionObserver((entries) => {
        entries.map((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.remove("lazy");
                observer.unobserve(entry.target);
            }
        });
    });
    images.forEach((image) => observer.observe(image));
}


function loadErrorPopup(html, statusCode) {
    spinner.stop()
    const error = document.createElement("p")
    error.innerHTML = html;
    document.querySelector('#error .inner').replaceChildren(error)
    document.querySelector('#error').classList.add("show")
    const bugReportLink = document.querySelector('#error p a.bug')
    if (bugReportLink) {
        bugReportLink.onclick = copyErrorDataAndRedirectToDiscord
    }
}

function fetchPlayerAdvice() {
    fetch("/results", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(fetchStoredUserParams())
    }).then(response => {
        return response.text().then(text => [text, (response.ok ? 200 : response.status)]);
    }).then(([html, statusCode]) => {
        switch (statusCode) {
            case 400:
            case 403:
            case 404:
            case 500:
                loadErrorPopup(html, statusCode)
                break;
            case 200:
                if (html === "") {
                    openSidebarIfFirstAccess();
                    return;
                }
                loadResults(html);
                initResultsUI();
                break;
            default:
                throw new Error(statusCode.toString());
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}

const storeUserParams = (data) => Object
    .entries(defaults)
    .forEach(([k, v]) => localStorage.setItem(k, data[k] || v))

const fetchStoredUserParams = () => {
    const storedUserParams = Object.fromEntries(Object.entries(defaults).map(([k, v]) => [k, localStorage.getItem(k) || v]))
    const queryStringParams = new URLSearchParams(storedUserParams)
    if (storedUserParams.player.startsWith("{")) {
        // empty player if it's JSON
        queryStringParams.delete("player")
    }
    history.pushState(null, '', `?${queryStringParams}`)
    return storedUserParams
}

function storeGetParamsIfProvided() {
    const GETData = new URLSearchParams(window.location.search);
    const truthy = [true, "True", "true", "on"]
    const falsy = [false, "False", "false", "off"]
    const params = {...defaults, ...Object.fromEntries(GETData.entries())}

    if (!GETData.size) return

    Object.entries(params).forEach(([k, v]) => {
        localStorage.setItem(k, truthy.includes(v) ? "on" : falsy.includes(v) ? "off" : v)
    })
}

function hideSpinnerIfFirstAccess() {
    if (!localStorage.getItem('player'))
        return
    var target = document.querySelector('#top');
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

function setupErrorPopup() {
    document.querySelector('#close-modal-error').onclick = () => {
        document.querySelector('#error').classList.remove("show")
        openSidebarIfFirstAccess()
    }
}

function collectTextNodes(parent) {
    const nodes = []

    for (const child of parent.childNodes) {
        if (child.nodeType === Node.TEXT_NODE) {
            nodes.push(child.textContent)
        } else if (child.nodeType === Node.ELEMENT_NODE) {
            nodes.push(...collectTextNodes(child))
        }
    }

    return nodes
}

function copyErrorDataAndRedirectToDiscord(e) {
    e.preventDefault()
    const error = document.querySelector('#error .wrapper');
    const errorText = document.querySelector('#error p');
    const errorTextBare = collectTextNodes(errorText).join(' ').replace(/ +/g, ' ');
    const logPath = document.querySelector('#error code').innerText
    const [server, type, name, timestamp] = logPath.split(" ▸ ")

    navigator.clipboard.writeText(`server: ${server}\ntype: ${type}\nname: ${name}\ntimestamp: ${timestamp}\n\n> ${errorTextBare}`)

    const copied = document.querySelector('#copied')
    const errorPos = error.getBoundingClientRect()
    copied.style.position = 'absolute'
    copied.style.left = `${e.pageX - errorPos.left}px`
    copied.style.top = `${e.pageY - errorPos.top}px`
    copied.classList.add('show')
    setTimeout(() => {
        const link = e.target.href
        window.open(link, '_blank').focus()
        copied.classList.remove('show')
    }, 1000)
}

function allHidden(siblings) {
    return [...siblings].every(
        sibling => [...sibling.classList].every(className => className.startsWith('hidden-'))
    );
}

function hideEmptySubgroupTitles(adviceGroup, classToHide) {
    const table = adviceGroup.querySelector('.table');
    const adviceTitles = table.querySelectorAll('.advice-title');
    const titleGroups = []

    // Group siblings under each '.advice-title'
    adviceTitles.forEach((title, index) => {
        // Find the next '.advice-title' or the end of the '.table'
        let nextTitleOrEnd = adviceTitles[index + 1] || table.lastElementChild;

        let advices = []
        let sibling = title.nextElementSibling;
        while (sibling && sibling !== nextTitleOrEnd) {
            advices.push(sibling); // Add sibling to this title's group
            sibling = sibling.nextElementSibling;
        }
        titleGroups.push([title, advices])
    });

    // Loop over each title group and check the visibility condition
    for (const [title, groupedAdvice] of titleGroups) {
        // If no visible siblings are found, add `classToHide` class to the title
        title.classList.toggle(classToHide, allHidden(groupedAdvice));
    }
}

const hidableElements = [
    "article",
    "section",
    ".advice-group",
    ".advice-title",
    ".advice", ".resource", ".prog", ".arrow", ".arrow-hidden", ".goal"
];

function hideComposite(event) {
    const slider = event.currentTarget,
        classToHide = slider.dataset.hides,
        checkboxOn = document.querySelector(`#hide_${classToHide}`).value === "on",
        queryString = hidableElements.map(cls => `${cls}.${checkboxOn ? '' : 'hidden-'}${classToHide}`).join(', '),
        allElements = document.querySelectorAll(queryString);

    allElements.forEach(el => el.classList.toggle(`hidden-${classToHide}`, checkboxOn));

    // the following recursive hiding logic is only necessary if we're hiding elements. Unhiding is easy.
    if (!checkboxOn) return

    const groups = document.querySelectorAll(".advice-group");

    groups.forEach(g => {
        hideEmptySubgroupTitles(g, `hidden-${classToHide}`);
        const allAdviceHidden = allHidden(g.querySelectorAll('.advice'));
        g.classList.toggle(classToHide, allAdviceHidden)
    });

    const sections = document.querySelectorAll("section");

    sections.forEach(s => {
        const allGroupsHidden = allHidden(s.querySelectorAll('.advice-group'));
        s.classList.toggle(classToHide, allGroupsHidden)
    });

    const worlds = document.querySelectorAll("article");

    worlds.forEach(w => {
        const allSectionsHidden = allHidden(w.querySelectorAll('section'));
        w.classList.toggle(classToHide, allSectionsHidden)
    });
}


let searchTimer

function searchByCriteria(criteria) {
    criteria = criteria.toLowerCase()
    const allElements = document.querySelectorAll("article, section, .advice-group, .advice-title, .advice, .resource, .prog, .arrow, .arrow-hidden, .goal")
    allElements.forEach(el => {
        el.classList.add('search-hidden');
    })
    allElements.forEach(el => {
        if (el.tagName.toLowerCase() === 'article') {
            if (el.querySelector("h1").innerHTML.toLowerCase().includes(criteria)) {
                el.classList.remove("search-hidden")
                el.querySelectorAll('.search-hidden').forEach(child => child.classList.remove("search-hidden"))
            }
        } else if (el.tagName.toLowerCase() === 'section') {
            if (el.querySelector("h1").innerHTML.toLowerCase().includes(criteria)) {
                el.closest("article").classList.remove("search-hidden")
                el.classList.remove("search-hidden")
                el.querySelectorAll('.search-hidden').forEach(child => child.classList.remove("search-hidden"))
            }
        } else if (el.classList.contains('advice-group')) {
            if (el.children.length > 0 && el.children[0].tagName.toLowerCase() === "span" && el.children[0].innerHTML.toLowerCase().includes(criteria)) {
                el.closest("article").classList.remove("search-hidden")
                el.closest("section").classList.remove("search-hidden")
                el.classList.remove("search-hidden")
                el.querySelectorAll('.search-hidden').forEach(child => child.classList.remove("search-hidden"))
            }
        } else if (el.classList.contains('advice')) {
            if (el.innerHTML.toLowerCase().includes(criteria)) {
                el.closest("article").classList.remove("search-hidden")
                el.closest("section").classList.remove("search-hidden")
                el.closest(".advice-group").classList.remove("search-hidden")
                el.classList.remove("search-hidden")
                const row = Array.from(el.parentElement.children)
                row.slice(row.indexOf(el) - 1, row.indexOf(el) + 5).forEach(col => {
                    col.classList.remove("search-hidden")
                })
                row.toReversed().slice(row.toReversed().indexOf(el)).find(col => col.classList.contains("advice-title"))?.classList.remove("search-hidden")
            }
        }
    })
}

function setupSearchBar() {
    const searchBar = document.querySelector('#search')
    document.querySelector('#search-clear').onclick = () => {
        searchBar.value = ""
        hideProgressBoxes()
        document.querySelectorAll('.search-hidden').forEach(hidden => {
            hidden.classList.remove('search-hidden')
        })
        calcProgressBars()
    }

    searchBar.addEventListener('input', e => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout((criteria) => {
            hideProgressBoxes()
            searchByCriteria(criteria)
            calcProgressBars()
        }, 1000, e.target.value)
    })
}

function delJSBlockedModal() {
    document.querySelector('#javascript-blocked').remove()
}

function initBaseUI() {
    delJSBlockedModal()
    setTimeout(defineCookieModalAction, 1000)
    hideSpinnerIfFirstAccess()
    defineFormSubmitAction()
    setupLightSwitch()
    setupSidebarToggling()
    setupSubmitKeybind()
    setTextareaDefaultFocusAction()
    setupColorScheme()
    setupToggleAllAction()
    setupSwitchesActions()
    setupErrorPopup()
    setupSearchBar()
}

function initResultsUI() {
    setFormValues()
    setupFolding()
    setupHrefEventActions()
    applyShowMoreButton()
    setupDataClock()
    calcProgressBars(document)
}

document.addEventListener("DOMContentLoaded", () => {
    // Define the fonts you are loading
    const fonts = ['Kode Mono', 'Open Sans', 'Rubik', 'Roboto']
    const loadedFonts = fonts.map(f => new FontFaceObserver(f).load())

    // Wait for all fonts to be loaded
    Promise.all(loadedFonts).then(() => {
        // Fonts are loaded, now run your code
        storeGetParamsIfProvided();
        initBaseUI();
        fetchPlayerAdvice();
    }).catch(() => {
        console.error('One or more fonts failed to load.');
        // You can still run your code here or handle the error
        storeGetParamsIfProvided();
        initBaseUI();
        fetchPlayerAdvice();
    });
});
