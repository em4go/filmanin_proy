const $ = (id) => {
    return document.getElementById(id)
}

let slider = $("year-selector")
let year = $("year-text")


if (slider) {
    slider.addEventListener('input', () => {
        year.innerText = slider.value
    })
}
