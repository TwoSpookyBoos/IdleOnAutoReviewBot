document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.banner:not(.no-collapse)').forEach((banner) => banner.onclick = (e) => e.currentTarget.parentElement.querySelectorAll('.content-wrapper').forEach(ul => ul.classList.toggle('folded')))
    document.querySelectorAll('.subheading:not(.no-collapse)').forEach((picture) => picture.onclick = (e) => {
        e.currentTarget.nextElementSibling.querySelectorAll('ul, em').forEach(ul => ul.classList.toggle('folded'))
        e.currentTarget.querySelector('img').classList.toggle('folded')
    })
    document.querySelectorAll('strong').forEach((title) => title.onclick = (e) => e.currentTarget.parentElement.querySelectorAll('ul').forEach(e => e.classList.toggle('folded')))
    document.querySelectorAll('strong:first-child').forEach((title) => title.onclick = (e) => {
        e.currentTarget.parentElement.querySelectorAll('ul').forEach(e => e.classList.toggle('folded'))
        e.currentTarget.parentElement.parentElement.querySelector('.subheading > img').classList.toggle('folded')
        let notice = e.currentTarget.querySelector('em')
        if (notice !== null) {
            notice.classList.toggle('folded')
        }
    })
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

    if (document.querySelectorAll('main, .error').length === 0) {
        let button = document.getElementById('handle-image');
        let clickEvent = new MouseEvent('click', {
            'view': window,
            'bubbles': true,
            'cancelable': true
        });
        button.dispatchEvent(clickEvent);
    }
});
