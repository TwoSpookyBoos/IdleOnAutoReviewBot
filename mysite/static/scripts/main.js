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

function progWidth(bar, w, p, g) {
    const goal = g.innerText.replace(/.*?(\d+).*/, "$1")
    const prog = p.innerText.replace(/.*?(\d+).*/, "$1")
    const inPercentages = g.innerText.includes("%") || p.innerText.includes("%")
    const inRatio = prog.length > 0 && goal.length > 0

    if (inRatio) return [(100 * parseFloat(prog) / parseFloat(goal)), true]
    if (inPercentages) return [parseFloat(prog) || parseFloat(goal), true]
    return [0, (inPercentages || inRatio)]
}

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

    // toggle progress bars
    document.querySelector('#progress_bars').onclick = e => {
        const checkbox= e.currentTarget
        document.querySelectorAll('.progress-box').forEach(box => {
            const siblings = Array.from(box.parentElement.children)
            const idx = siblings.indexOf(box)
            const prog = siblings[idx + 2]
            const goal = siblings[idx + 4]
            const row = siblings.slice(idx + 1, idx + 5)
            const rowWidth = row.reduce((total, curr) => total + curr.offsetWidth, 0)
            const [_, show] = progWidth(box, rowWidth, prog, goal)

            if (checkbox.value === "off") {
                box.classList.add('hidden')
            } else if (show) {
                box.classList.remove('hidden')
            }
        })
    }

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
        const groups = Array.from(expandableGroups.querySelectorAll(".advice-group.hidden"))

        showMoreButton.style.display = (groups.length > 0) ? "block" : "none"

        showMoreButton.onclick = e => {
            const button = e.currentTarget

            groups.shift().classList.remove("hidden")

            if (groups.length === 0) {
                button.style.display = "none"
            }
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
    // data age clock
    setInterval(() => {
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

    // add progress bars
    document.querySelectorAll(".progress-box").forEach(progressBox => {
        const progressBar = progressBox.children[0]
        const advice = progressBox.nextElementSibling
        const siblings = Array.from(advice.parentElement.children)
        const idx = siblings.indexOf(advice)
        const prog = siblings[idx + 1]
        const goal = siblings[idx + 3]
        const row = siblings.slice(idx, idx + 4)
        const rowWidth = row.reduce((total, curr) => total + curr.offsetWidth, 0)
        const rowHeight = advice.offsetHeight
        const rowRect = advice.getBoundingClientRect()
        const rowTop = rowRect.top - advice.parentElement.getBoundingClientRect().top
        const [progCoefficient, show] = progWidth(progressBox, rowWidth, prog, goal)

        progressBox.style.height = `${rowHeight}px`
        progressBar.style.width = `${progCoefficient}%`
        progressBox.style.top = `${rowTop}px`

        if (!show) progressBox.classList.add("hidden")
    })
});
