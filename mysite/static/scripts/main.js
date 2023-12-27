document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('h1, h3').forEach((banner) => banner.onclick = (e) => e.currentTarget.nextElementSibling.classList.toggle('folded'))
    document.querySelector('aside > button').onclick = () => document.body.classList.toggle('light-mode')
    document.querySelector('#drawer-handle').onclick = (e) => {
        e.currentTarget.classList.toggle('sidebar-open')
        document.querySelector('aside').classList.toggle('sidebar-open')
    }
    const runColorMode = (fn) => {
        if (!window.matchMedia) return
        const query = window.matchMedia('(prefers-color-scheme: light)')
        fn(query.matches)
        query.addEventListener('change', (event) => fn(event.matches))
    }

    const body = document.body.classList
    const cls = 'light-mode'
    runColorMode((isLightMode) => isLightMode ? body.add(cls) : body.remove(cls))

    if (document.querySelector('main') === null) {
        document.querySelectorAll('aside, #drawer-handle').forEach((e) => e.classList.add('sidebar-open'))
    }
});
