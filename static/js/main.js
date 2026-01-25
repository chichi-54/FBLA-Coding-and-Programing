
//GET SEARCH FORM AND PAGE LINKS
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')
// clear review

const reviewForm = document.getElementById('reviewForm')

if (reviewForm) {
    reviewForm.addEventListener('submit', function () {
        setTimeout(() => {
            this.reset()
        }, 100)
    })
}


// hover
document.addEventListener("DOMContentLoaded", () => {
    const preview = document.getElementById("hover-preview")
    const previewImg = document.getElementById("hover-img")
    const gallery = document.querySelector(".business__gallery")

    if (!preview || !previewImg || !gallery) return

    document.querySelectorAll(".gallery-item img").forEach(img => {
        img.addEventListener("mouseenter", () => {
            previewImg.src = img.src
            preview.style.display = "block"

            const imgRect = img.getBoundingClientRect()
            const galleryRect = gallery.getBoundingClientRect()

            preview.style.top = (imgRect.top - galleryRect.top) + "px"
        })

        img.addEventListener("mouseleave", () => {
            preview.style.display = "none"
        })
    })
})


// delete 
document.addEventListener("DOMContentLoaded", function() {

    // --- Delete existing images ---
    document.querySelectorAll(".delete-image-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            const imgDiv = btn.parentElement
            const imgId = btn.dataset.id

            // Mark for deletion: append a hidden input
            const input = document.createElement("input")
            input.type = "hidden"
            input.name = "delete_images"
            input.value = imgId
            document.querySelector("form").appendChild(input)

            // Remove image preview from DOM
            imgDiv.remove()
        })
    })

    // --- Add new image dynamically ---
    const container = document.getElementById("new-images-container")
    const addBtn = document.getElementById("add-new-image")

    addBtn.addEventListener("click", () => {
        const input = document.createElement("input")
        input.type = "file"
        input.name = "new_images"
        input.className = "new-image-input"
        container.appendChild(input)
    })

    // --- Category Pills (same as before) ---
    const selected = new Set()
    const hiddenInput = document.getElementById('selectedCategories')
    const otherField = document.getElementById('otherCategoryField')

    document.querySelectorAll('.business-tag').forEach(tag => {
        const id = tag.dataset.id
        if (tag.classList.contains('selected')) selected.add(id)

        tag.addEventListener('click', () => {
            if (selected.has(id)) {
                selected.delete(id)
                tag.classList.remove('selected')
            } else {
                selected.add(id)
                tag.classList.add('selected')
            }

            otherField.style.display = selected.has('other') ? 'block' : 'none'
            hiddenInput.value = [...selected].filter(i => i !== 'other').join(',')
        })
    })
    hiddenInput.value = [...selected].filter(i => i !== 'other').join(',')
})

// categories
document.addEventListener("DOMContentLoaded", function() {
    const selected = new Set()
    const hiddenInput = document.getElementById('selectedCategories')
    const otherField = document.getElementById('otherCategoryField')
    const categoryPills = document.querySelectorAll('.business-tag')

    // --- Pre-select categories from backend ---
    // 'preSelected' should be a list of IDs passed via template
    if (typeof preSelected !== "undefined" && Array.isArray(preSelected)) {
        preSelected.forEach(id => selected.add(String(id)))
    }

    // If Other categories exist, select Other pill
    if (typeof hasCustomCategories !== "undefined" && hasCustomCategories) {
        selected.add('other')
    }

    // Apply 'selected' class to DOM pills
    categoryPills.forEach(tag => {
        const id = tag.dataset.id
        if (selected.has(id)) {
            tag.classList.add('selected')
        }

        // Toggle selection on click
        tag.addEventListener('click', () => {
            if (selected.has(id)) {
                selected.delete(id)
                tag.classList.remove('selected')
            } else {
                selected.add(id)
                tag.classList.add('selected')
            }

            // Show / hide Other textarea
            if (selected.has('other')) {
                otherField.style.display = 'block'
            } else {
                otherField.style.display = 'none'
            }

            // Only real category IDs go to Django
            const realIds = [...selected].filter(i => i !== 'other')
            hiddenInput.value = realIds.join(',')
        })
    })

    // Initialize hidden input on page load
    hiddenInput.value = [...selected].filter(i => i !== 'other').join(',')
})


//ENSURE SEARCH FORM EXISTS
if (searchForm) {
    for (let i = 0; pageLinks.length > i; i++) {
        pageLinks[i].addEventListener('click', function (e) {
            e.preventDefault()

            //GET THE DATA ATTRIBUTE
            let page = this.dataset.page

            //ADD HIDDEN SEARCH INPUT TO FORM
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`


            //SUBMIT FORM
            searchForm.submit()
        })
    }
}



let tags = document.getElementsByClassName('project-tag')

for (let i = 0; tags.length > i; i++) {
    tags[i].addEventListener('click', (e) => {
        let tagId = e.target.dataset.tag
        let projectId = e.target.dataset.project

        // console.log('TAG ID:', tagId)
        // console.log('PROJECT ID:', projectId)

        fetch('http://127.0.0.1:8000/api/remove-tag/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'project': projectId, 'tag': tagId })
        })
            .then(response => response.json())
            .then(data => {
                e.target.remove()
            })

    })
}
