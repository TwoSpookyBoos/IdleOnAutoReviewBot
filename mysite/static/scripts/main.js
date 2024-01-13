document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.banner:not(.no-collapse), .subheading').forEach((banner) => banner.onclick = (e) => e.currentTarget.nextElementSibling.classList.toggle('folded'))
    document.querySelector('#light-switch').onclick = (e) => {
        document.body.classList.toggle('light-mode')
        e.currentTarget.classList.toggle('on')
        e.currentTarget.classList.toggle('off')
    }
    document.querySelector('#handle-image').onclick = (e) => {
        document.querySelectorAll('aside, #handle-image').forEach(e => e.classList.toggle('sidebar-open'))
    }

    const runColorMode = (fn) => {
        if (!window.matchMedia) return
        const query = window.matchMedia('(prefers-color-scheme: light)')
        fn(query.matches)
        query.addEventListener('change', (event) => fn(event.matches))
    }

    const body = document.body.classList
    const cls = 'light-mode'
    runColorMode((isLightMode) => {
        let lightSwitch = document.querySelector('#light-switch')
        isLightMode ? body.add(cls) : body.remove(cls)
        lightSwitch.classList.add(isLightMode ? 'on' : 'off')
    })

    if (document.querySelector('main') === null) {
        let button = document.getElementById('handle-image');
        let clickEvent = new MouseEvent('click', {
            'view': window,
            'bubbles': true,
            'cancelable': true
        });
        button.dispatchEvent(clickEvent);
    }
});
