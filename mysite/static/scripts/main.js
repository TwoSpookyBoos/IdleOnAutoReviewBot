function toggleSidebar() {
    document.querySelectorAll('#drawer, #drawer-handle').forEach(e => e.classList.toggle('sidebar-open'))
}

// close the sidebar if clicked outside of it or not on hamburger
document.addEventListener("click", (e) => {
    let drawer = e.target.closest("#drawer") || e.target.closest("#drawer-handle")
    let  sidebar = document.getElementById("drawer")
    if (drawer === null && sidebar.classList.contains("sidebar-open")) {
        toggleSidebar()
    }
})

// close the sidebar if it's open and Esc key is pressed
document.addEventListener("keydown", (e) => {
    let escPressed = e.code === "Escape"
    if (escPressed) toggleSidebar()
})

document.addEventListener("DOMContentLoaded", () => {
    // set event listeners for folding worlds and sections
    document.querySelectorAll('.toggler').forEach(toggler => toggler.onclick = (e) => {
        let title = e.currentTarget
        for (const element of [title, title.nextElementSibling]) {
            element.classList.toggle("folded")
        }
    })

    document.querySelector('#light-switch').onclick = (e) => {
        document.documentElement.classList.toggle('light-mode')
        e.currentTarget.classList.toggle('on')
        e.currentTarget.classList.toggle('off')
    }
    document.querySelector('#drawer-handle').onclick = toggleSidebar

    // submit the form content if the text area is focused and (Ctrl|Cmd) + Enter is pressed
    document.querySelector("textarea[name='player']").addEventListener("keypress", e => {
        let ctrlCmdPressed = e.ctrlKey || e.metaKey
        let enterPressed = e.code === "Enter"

        if (! (ctrlCmdPressed && enterPressed)) return

        let clickEvent = new MouseEvent('click', {
            'view': window,
            'bubbles': true,
            'cancelable': true
        });
        document.querySelector('input[type="submit"]').dispatchEvent(clickEvent);
    })

    const runColorMode = (fn) => {
        if (!window.matchMedia) return
        const query = window.matchMedia('(prefers-color-scheme: light)')
        fn(query.matches)
        query.addEventListener('change', (event) => fn(event.matches))
    }

    const body = document.documentElement.classList
    const cls = 'light-mode'
    runColorMode((isLightMode) => {
        let lightSwitch = document.querySelector('#light-switch')
        isLightMode ? body.add(cls) : body.remove(cls)
        lightSwitch.classList.add(isLightMode ? 'on' : 'off')
    })

    // show sidebar if opening the page for the first time
    if (document.querySelectorAll('main, .error').length === 0) {
        toggleSidebar()
    }

    // change colour and position of switches when clicked
    document.querySelectorAll('#switchbox label').forEach(label => label.onclick = e => {
        const lbl = e.currentTarget
        const shaft = lbl.querySelector(".shaft")
        shaft.classList.toggle("on")
        shaft.classList.toggle("off")
        const checkbox = lbl.previousElementSibling
        checkbox.value = checkbox.value === "on" ? "off" : "on"
    })

    // handle left/right handedness switching
    document.querySelector('#handedness').onclick = () => document.querySelectorAll('.slider, .nav-links, #drawer-handle').forEach(s => s.classList.toggle('lefty'))

    document.querySelectorAll('#pinchy .advice-group a').forEach(hyperlink => hyperlink.onclick = e => {
        const link = e.currentTarget
        const targetId = link.getAttribute("href").slice(1)
        const target = document.querySelector(`#${targetId}`)
        target.parentElement.classList.remove('folded')
        target.querySelectorAll('*:not(.empty)').forEach(c => c.classList.remove('folded'))
    })
    const expandableSections = document.querySelectorAll("#gem-shop .advice-section, #greenstacks .advice-section, #cards .advice-section")
    expandableSections.forEach(section => {
        const expandableGroups = section.querySelector(".groups")
        const showMoreButton = section.querySelector(".show-more")
        showMoreButton.onclick = e => {
            const button = e.currentTarget
            const groups = expandableGroups.querySelectorAll(".hidden")

            groups[0].classList.remove("hidden")
            if (groups.length === 1) {
                button.style.display = "none"
            }

        }
        if (expandableGroups.children.length > 3) {
            showMoreButton.style.display = "block"
        }
    })

    document.querySelectorAll('.collapse-cards').forEach(title => title.onclick = e => {
        const t = e.currentTarget
        const siblings = Array.from(t.parentElement.children)
        const index = siblings.indexOf(t)
        siblings.forEach(sib => {
            if (sib === t) return
            sib.classList.toggle('folded')
        })
    })
});
