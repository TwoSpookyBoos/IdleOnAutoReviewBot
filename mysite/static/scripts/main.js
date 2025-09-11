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
    library_group_characters: "off",
    hide_overwhelming: "off",
    hide_optional: "off",
    hide_completed: "off",
    hide_informational: "off",
    hide_unrated: "off",
    progress_bars: "off",
    tabbed_advice_groups: "on",
    handedness: "off",
    light: "off"
}

const spinner = new Spin.Spinner(opts)

const isDesktop = window.matchMedia('(min-width: 768px)').matches;

function toggleSidebar() {
    document.querySelectorAll('#drawer, #drawer-handle, #veil')
        .forEach(e => e.classList.toggle('sidebar-open'))
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
    document.querySelector('#light-switch').onclick = e => {
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
        const drawerClicked = e.target.closest("#drawer") || e.target.closest("#drawer-handle") || e.target.id === "close-modal-error",
            sidebarOpened = document.getElementById("drawer").classList.contains("sidebar-open");
        if (!drawerClicked && sidebarOpened) {
            toggleSidebar()
        }
    })

    // close the sidebar if it's open and Esc key is pressed
    document.addEventListener("keydown", (e) => {
        const escPressed = e.code === "Escape",
            searchOpen = document.querySelector("#searchbar-wrapper").classList.contains("search-open"),
            settingsOpen = document.querySelector("#dynamic-switchbox-wrapper").classList.contains("open");

        if (!escPressed) return;

        if (searchOpen) {
            document.querySelector("#searchbar-wrapper").classList.remove("search-open");
        } else if (settingsOpen) {
            document.querySelector("#dynamic-switchbox-wrapper").classList.remove("open");
            // fucker won't go under the backdrop...
            document.querySelector("#drawer-handle").style.zIndex = "98"
        } else {
            toggleSidebar();
        }
    })
}

function setupSubmitKeybind() {
    // submit the form content if the text area is focused and (Ctrl|Cmd) + Enter is pressed
    document.querySelector("textarea[name='player']").addEventListener("keypress", e => {
        const ctrlCmdPressed = e.ctrlKey || e.metaKey
        const enterPressed = e.code === "Enter"

        if (!(ctrlCmdPressed && enterPressed)) return

        const clickEvent = new MouseEvent('click', {
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
    document.querySelector('#progress_bars').onclick = () => document.querySelectorAll(".progress-box").forEach(progressBox => {
        const checkbox = document.querySelector('#progress_bars')
        if (checkbox.value === "off") {
            progressBox.classList.add('hidden')
        } else {
            progressBox.classList.remove('hidden')
        }
    })

    // On Click Listener for the Hide Overwhelming switch
    document.querySelector('label[for="hide_overwhelming"]').addEventListener('click', hideComposite);

    // On Click Listener for the Hide Optional switch
    document.querySelector('label[for="hide_optional"]').addEventListener('click', hideComposite);

    // On Click Listener for the Hide Completed switch
    document.querySelector('label[for="hide_completed"]').addEventListener('click', hideComposite);

    // On Click Listener for the Hide Info switch
    document.querySelector('label[for="hide_informational"]').addEventListener('click', hideComposite);

    // On Click Listener for the Hide Info switch
    document.querySelector('label[for="hide_unrated"]').addEventListener('click', hideComposite);
}

function setupHrefEventActions() {
    addEventListener("hashchange", () => {
        const h = location.hash.slice(1) || "pinchy-all" // Defaults on the pinchy section if you try to access an empty hash, for exemple when hiting return on your browser
        const target = (document.getElementById(h) || document.getElementsByName(h)[0] || document.body)
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
    const [sectionH1, sectionDiv] = findSectionElements(target)
    const [articleH1, articleDiv] = findArticlesElements(target);
    const articleElement = articleDiv?.parentElement;

    if (articleDiv?.classList.contains('folded')) {
        // The section is folded, we need to wait until the transition is complete to scroll to its position
        const onTransitionEnd = evt => {
            if (evt.target === articleDiv) { // Multiple events are triggered, we only want the article div one
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
    const div = target.closest('div.collapse-wrapper:has(> div.sections)') || document.querySelector('div.collapse-wrapper:has(> div.sections)');
    const h1 = div.parentElement.querySelector('h1.banner.toggler');
    return [h1, div]
}

function findSectionElements(target) {
    const div = target.closest('div.collapse-wrapper:has(> ul.advice-section)') || target.querySelector('div.collapse-wrapper:has(> ul.advice-section)');
    const h1 = div.parentElement.querySelector('h1.subheading.toggler')
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

function hideElements() {
    ["optional", "completed", "informational", "unrated", "overwhelming"].forEach(cls => hideComposite({
        currentTarget: document.querySelector(`[data-hides="${cls}"]`)
    }));
}

function setFormValues() {
    const form = document.querySelector('form')
    const userParams = fetchStoredUserParams()

    Object.entries(defaults).forEach(([k, v]) => {
        const userValue = userParams[k] ?? v
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
    console.log(`error ${statusCode}`)
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
                initialize_tabbed_advice_group_logic();
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
    .forEach(([k, v]) => localStorage.setItem(k, data[k] ?? (v === "on" ? "off" : v)))

const fetchStoredUserParams = () => {
    const storedUserParams = Object.fromEntries(Object.entries(defaults).map(([k, v]) => [k, localStorage.getItem(k) ?? v]))
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
    const target = document.querySelector('#top');
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

const kidsHiddenClass = "hidden-children-hidden";
const hiddenElements = {
    "hidden-completed": new Set(),
    "hidden-informational": new Set(),
    "hidden-unrated": new Set(),
    "hidden-overwhelming": new Set(),
    "hidden-optional": new Set(),
    [kidsHiddenClass]: new Set()
}

function allHidden(siblings) {
    if (siblings.length < 1) return false;

    const allHiddenElements = new Set();
    for (const set of Object.values(hiddenElements)) {
        for (const el of set) {
            allHiddenElements.add(el);
        }
    }

    for (const sib of siblings) {
        if (!allHiddenElements.has(sib)) return false;
    }
    return true;
}

function hideEmptySubgroupTitles(adviceGroup) {
    const table = adviceGroup.querySelector('.table');
    const adviceTitles = table.querySelectorAll('.advice-title');
    const siblings = [...table.children];

    // Group siblings under each '.advice-title', then hide titles if all their advices are hidden
    [...adviceTitles]
        .map((title, index) => {
            const titleIndex = siblings.indexOf(title),
                nextTitleIndexOrEnd = siblings.indexOf(adviceTitles[index + 1]),
                advices = siblings.slice(titleIndex + 1, nextTitleIndexOrEnd !== -1 ? nextTitleIndexOrEnd : undefined);
            return [title, advices];
        })
        .forEach(([title, groupedAdvice]) => {
            // If no visible siblings are found, add `classToHide` class to the title
            const allKidsHidden = allHidden(groupedAdvice);
            title.classList.toggle(kidsHiddenClass, allKidsHidden);
            if (allKidsHidden) {
                hiddenElements[kidsHiddenClass].add(title)
            } else {
                hiddenElements[kidsHiddenClass].delete(title)
            }
        })
}

function hideComposite(event) {
    const slider = event.currentTarget,
        classToHide = slider.dataset.hides,
        checkboxOn = document.getElementById(slider.getAttribute("for")).value === "on",
        hiddenClass = `hidden-${classToHide}`,
        hiddenAttr = `[data-${classToHide}="true"]`,
        queryString = checkboxOn ? hiddenAttr : `.${hiddenClass}`,
        allElements = document.querySelectorAll(queryString);

    if (!checkboxOn) {
        hiddenElements[hiddenClass].forEach(e => e.classList.remove(hiddenClass));
        hiddenElements[hiddenClass].clear();
    } else {
        allElements.forEach(el => el.classList.add(hiddenClass));
        hiddenElements[hiddenClass] = new Set([...allElements])
    }

    const elementsToRecurse = [
        ["article", "section"],         // hide world if all sections within are hidden
        ["section", ".advice-group"],   // hide section if all advice groups within are hidden
        [".advice-group", ".advice"]    // hide advice group if all pieces of advice within are hidden
    ].reverse() // has to be processed in reverse order (deeper nested elements first), but writing it out in this order makes it more readable

    // first handle subgroup titles
    for (const element of document.querySelectorAll(elementsToRecurse[0][0])) {
        hideEmptySubgroupTitles(element, hiddenClass)
    }

    // recurse through groups, sections, and worlds and hide them if needed
    elementsToRecurse.forEach(([parentStr, childStr]) => {
        document.querySelectorAll(parentStr).forEach(parent => {
            const shouldHide = allHidden(parent.querySelectorAll(childStr));
            parent.classList.toggle(kidsHiddenClass, shouldHide)
        });
    })

    recalculate_tab_selections()
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
                row.slice(row.indexOf(el), row.indexOf(el) + 5).forEach(col => {
                    col.classList.remove("search-hidden")
                })
                row.toReversed().slice(row.toReversed().indexOf(el)).find(col => col.classList.contains("advice-title"))?.classList.remove("search-hidden")
            }
        }
    })
}

function setupSearchBar() {
    const searchBar = document.querySelector('#search');

    document.querySelector('#search-clear').onclick = () => {
        searchBar.value = ""
        document.querySelectorAll('.search-hidden').forEach(hidden => {
            hidden.classList.remove('search-hidden')
        })
    };

    searchBar.addEventListener("keyup", e => {
        if (e.key !== "Enter") return;
        searchByCriteria(e.currentTarget.value);
        document.querySelector("#searchbar-wrapper").classList.remove('search-open');
    });
    document.querySelector("#searchbar-wrapper").addEventListener('click', e => e.target.classList.remove("search-open"))
    document.querySelector("#magnifier").onclick = () => {
        document.querySelector("#searchbar-wrapper").classList.toggle('search-open')
        document.querySelector('#search').focus();
    };
}

function setupSwitchBox() {
    const switchBox = document.querySelector("#dynamic-switchbox-wrapper");
    switchBox.addEventListener('click', e => {
        e.target.classList.remove("open")
    })
    document.querySelector("#settings").onclick = () => {
        // fucker won't go under the backdrop...
        document.querySelector("#drawer-handle").style.zIndex = "97"

        switchBox.classList.toggle('open')
    };
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
    setupSwitchBox()
}

function initResultsUI() {
    setFormValues()
    setupFolding()
    setupHrefEventActions()
    applyShowMoreButton()
    setupDataClock()
    hideElements()
    handleParallax()
    animateStaleData()
}

function handleParallax() {
    const background = document.getElementById('backgrounds');

    let dominantElement = null;
    let dominantBackground = null;

    const switchBackground = () => {
        Array.from(background.children).forEach(bg => bg.style.opacity = "0");
        if (dominantBackground === undefined){
            return;
        }
        const backgroundToFocus = document.getElementById(dominantElement.bg);
        if (backgroundToFocus) {
            backgroundToFocus.style.opacity = "1";
        }
        dominantBackground = backgroundToFocus;
    }

    const translateBackground = () => {
        const bgHeight = background.getBoundingClientRect().height;
        const bgHeightDiff = (bgHeight - window.innerHeight) / bgHeight * 100;
        const focusedArticle = dominantElement.article
        const scrollPercentage = (dominantElement.top - window.innerHeight / 2) / -focusedArticle.scrollHeight;
        dominantBackground.style.transform = `translateY(-${scrollPercentage * bgHeightDiff}%)`;
    }

    const findDominantElement = () => {
        const screenCenter = window.innerHeight / 2;

        dominantElement = Array.from(document.querySelectorAll("article"))
        .map(article => {
            const rect = article.getBoundingClientRect();
            return { bg: `bg-${article.id}`, article: article, top: rect.top, bottom: rect.bottom, height: rect.height };
        })
        .find(article => {
            const dominatesTop = article.top <= 0 && article.bottom > screenCenter;
            const dominatesMiddle = article.top >= 0 && article.bottom <= window.innerHeight && article.height >= screenCenter;
            const dominatesBottom = article.top <= screenCenter && article.bottom > window.innerHeight;
            return dominatesTop | dominatesMiddle | dominatesBottom;
        });
    }

    const updateParallax = () => {
        findDominantElement()
        switchBackground()
        if (dominantBackground) {
            translateBackground()
        }
    }

    document.querySelector('.container-fluid').onscroll = updateParallax;
    window.addEventListener('resize', updateParallax);
    updateParallax();
}

/* The animation for the old data needs to be triggered once the browser finishes with the
 * UI rendering/repainting, otherwise it can get executed inconsistently (start too early)
 */
function animateStaleData() {
    // I don't feel like making some contrived workarounds to make it look good on mobile
    if (!isDesktop) return;
    requestAnimationFrame(() => {
        setTimeout(() => {
            const staleDataElement = document.querySelector('.stale')
            if (staleDataElement) {
                document.querySelector('.stale').style.animation = 'shake 1s linear'
            }
        }, 0);
    });
}

function initialize_tabbed_advice_group_logic() {
    const tabGroups = document.querySelectorAll('.advice-group-tabbed');

    tabGroups.forEach(group => {
        const tabs = group.querySelectorAll('.advice-group-tabbed-tab');
        const contents = group.querySelectorAll('.advice-group-tabbed-tab-content');

        function deactivateAll() {
            tabs.forEach(tab => tab.classList.remove('tab-active'));
            contents.forEach(content => content.style.display = 'none');
        }

        deactivateAll();

        tabs.forEach((tab, index) => {
            tab.addEventListener('click', () => {
                deactivateAll();
                tab.classList.add('tab-active');
                contents[index].style.display = 'flex';
            });
        });
    });

    recalculate_tab_selections()
}

function recalculate_tab_selections() {
    const tabGroups = document.querySelectorAll('.advice-group-tabbed');

    tabGroups.forEach(group => {
        const tabs = group.querySelectorAll('.advice-group-tabbed-tab');
        const firstVisibleTab = Array.from(tabs).find(tab => tab.display !== "none")
        firstVisibleTab.click()
    });
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
