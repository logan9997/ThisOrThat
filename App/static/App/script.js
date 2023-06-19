function remove_placeholder_text(element) {
    element.placeholder = ''
}

function return_tags() {
    var tags_container = document.getElementById('created-tags').childNodes
    var tags_input = document.getElementById('tags-input')
    var tags_string = ''

    for (let i = 0; i < tags_container.length; i ++) {
        tags_string += tags_container[i].innerHTML.toLowerCase()
        if (i != tags_container.length - 1) {
            tags_string += ', '
        }
    }
    tags_input.value = tags_string

}

function seperate_tags(element) {
    var input_value = element.value;
    var tag = null;

    for (let i = 0; i < input_value.length; i ++) {
        if (input_value[i] == ',') {
            tag = input_value.slice(0, i)
            element.value = ''
            break
        }
    }

    if (tag != null) {
        // create new span containing the new tag
        var created_tags = document.getElementById('created-tags')
        var node = document.createElement('span')
        node.innerHTML = tag
        created_tags.appendChild(node)

        // calculate created-tags new width    
        tags_width = created_tags.style.width
        if (tags_width == '') {
            tags_width = `${tag.length}%`
        } else {
            tags_width = tags_width.replace('%', '')
            tags_width = parseInt(tags_width)
            tags_width = `${(tags_width + tag.length) * 2}%`
        }
        created_tags.style.width = tags_width
        created_tags.style.padding = '0.15rem'
        created_tags.style.border = '0.2px black solid;'


        // calculate inputs new width
        var input_width = element.style.width
        input_width = input_width.replace('%', '')
        input_width = parseInt(input_width)
        input_width = `${(input_width - tags_width) / 2}rem`

        element.style.width = input_width

    }
}

function remove_tag_param() {
    var newURL = location.href.split("?")[0];
    window.history.pushState('object', document.title, newURL);
    location.reload()
}

function search_suggestions() {
    var input = document.getElementById('tags-search')
    var tags = JSON.parse(document.getElementById('tags-list').textContent)
    var search_suggestions_container = document.getElementById('search-suggestions-container')
    const max_search_suggestions = JSON.parse(document.getElementById('max-search-suggestions').textContent)

    // clear search suggestions container before each oninput call
    for (let i = max_search_suggestions; i >= 0; i --) {
        console.log(search_suggestions_container.childNodes[i])
        if (search_suggestions_container.childNodes[i] != undefined) {
            search_suggestions_container.removeChild(search_suggestions_container.lastChild)
        } 
    }
    search_suggestions_container.style.padding = '0'
    search_suggestions_container.style.display = 'none'
    
    // create new containers for matched tags
    var matches = 0 
    for (let i = 0; i < tags.length; i ++ ) {
        if (tags[i].includes(input.value.toLowerCase()) && input.value != '') {
            var node = document.createElement('a')
            var tag = tags[i]
            var current_url = window.location.href

            if (tag[0] == ' ') {
                tag = tag.slice(1, tag.length)
            }

            if (current_url.includes('?')) {
                var question_mark_index = current_url.indexOf('?')
                current_url = current_url.slice(0, question_mark_index)
            }

            node.href = `${current_url}?tag=${tag}`
            node.innerHTML = tags[i]
            search_suggestions_container.appendChild(node)
            matches += 1
        }
        if (matches >= max_search_suggestions) {
            break
        }
        if (matches > 0) {
            search_suggestions_container.style.display = 'block'
            search_suggestions_container.style.padding = '0.1rem'
            search_suggestions_container.style.border = '0.1rem black solid'
            search_suggestions_container.style.borderTop = 'none'
        }
    }
}

function preview_uploaded_image(event, option) {
    var output = document.getElementById(`image-${option}-preview`);
    output.style.display = 'inline';
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src) 
    }
};

function show_remove_image_button(option) {
    document.getElementById(`remove-image-${option}-button`).style.display = 'block'
    document.getElementById(`image-${option}-input`).value = ''
}

function click_file_input(option) {
    document.getElementById(`image-${option}-input`).click()
}

function change_element_display(element, display) {
    document.getElementById(element).style.display = display
} 

function style_textareas_when_scroll_bar_visible() {
    var textareas = document.getElementsByTagName('textarea')
    for (let i = 0; i < textareas.length; i ++) {
        if (textareas[i].hasScrollBar()) {
            textareas[i].style.borderRadius = '0'
        }
    }
}