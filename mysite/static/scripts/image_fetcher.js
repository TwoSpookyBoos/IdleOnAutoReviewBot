// This is a generic script that fetches images from a specific wiki table (e.g. spices, chests)
// and formats them into a ready-to-use SCSS map. to do this, right-click on an image in a table, click inspect.
// The dev console will pop up, focused in the Elements tab on the image's HTML element. it should be the something like
// <img alt="Turkey a la Thank.png" 
//      src="/wiki/images/thumb/b/b9/Turkey_a_la_Thank.png/36px-Turkey_a_la_Thank.png"
//      ...
//      srcset="/wiki/images/b/b9/Turkey_a_la_Thank.png 1.5x"
// >
//
// Right-click it, click copy > Copy selector. Call the getImageMap function with the selector as parameter,
// don't forget to wrap it in quotes.
//
// in the ideal case the script will spit out something like
// $meals: (
//     turkey-a-la-thank: wiki(b/b9/Turkey_a_la_Thank.png),
//     ...
// );

String.prototype.toKebabCase = function () {
    return this.toLowerCase()
        .replaceAll(" ", "-")
        .replaceAll(/[^\w-]/g, '')
        .replaceAll(/-+/g, '-')
}

const getImageMap = (cssQuery, mapName_) => {
    // let cssQuery = "table.sortable > tbody > tr:nth-child(1) > td:nth-child(2) > div > div > a > img"
    // this will replace the reference to that specific row the image is located in to instead fetch all rows, except the first (header) row
    cssQuery = cssQuery.replace(/tr.*? /, 'tr:not(:first-child) ')

    // map all image names and their links into SCSS map records.
    // it may require change depending on the attributes of the image element.
    // some have only the `src` attribute, some don't, not sure, some have `srcset`, and some may not be matched by the regex.
    // some potentially don't have `alt`... it's not too tried and tested.
    const records = $(cssQuery).get().map(e => {
        const img = $(e);
        const link = img.attr('src').replace(/.*(\w+\/\w+\/\w+.png).*/, '$1')
        const name = img.attr('alt').slice(0, -4).toKebabCase()
        return `\t${name}: wiki("${link}")`
    })

    const mapName = `$${mapName_.toKebabCase()}`
    const map = `${mapName}: (\n${records.join(',\n')}\n);`

    console.log(map)
}

// this function will attempt to create multiple maps, one for each table found on the page
const collectAllTablesOnPage = () => {
    let cssQuery = "tbody > tr:nth-child(1) > td:nth-child(2) > div > div > a > img"
    cssQuery = cssQuery.replace(/tr.*? /, 'tr ')

    $("table.sortable").each((_, t) => {
        const records = $(t).find(cssQuery).get().map(e => {
            const img = $(e);
            const link = img.attr('src').replace(/.*(\w+\/\w+\/[\w%]+.png).*/, '$1')
            const name = img.attr('alt').slice(0, -4).toKebabCase()
            return `\t${name}: wiki("${link}")`
        })
        const mapName = $(t).find('caption > span:first-child').text().toKebabCase()
        const map = `$${mapName}: (\n${records.join(',\n')}\n);`
        console.log(map)
    })
}
