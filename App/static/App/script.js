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

function create_tag(tag) {
    var created_tags_container = document.getElementById('created-tags')
    var created_tags = created_tags_container.getElementsByTagName('button')
    var node = document.createElement('button')
    
    //set node attributes
    node.type = 'button'
    node.innerHTML = tag
    node.onclick = function() {
        for (let i = 0; i < created_tags.length; i ++) {
            if (created_tags[i].innerHTML == tag) {
                created_tags[i].remove()
            }
        }
        // checks there is atleast one tag
        validate_post_create_input(document.getElementById('create-post-form'))
    }
    created_tags_container.appendChild(node)

    // calculate created-tags new width    
    tags_width = created_tags_container.style.width
    if (tags_width == '') {
        tags_width = `${tag.length}%`
    } else {
        tags_width = tags_width.replace('%', '')
        tags_width = parseInt(tags_width)
        tags_width = `${(tags_width + tag.length) * 2}%`
    }
    created_tags_container.style.padding = '0.15rem'
    created_tags_container.style.border = '0.2px black solid;'
}

function seperate_tags(element) {
    var input_value = element.value;
    var tag = null;

    for (let i = 0; i < input_value.length; i ++) {
        if (input_value[i] == ',') {
            tag = input_value.slice(0, i)
            element.value = ''
            if (tag.length > 2) {
                create_tag(tag)
            }
            break
        }
    }
}

function update_textarea_chars(textarea) {
    var all_textareas = document.getElementsByTagName('textarea')
    all_textareas = Array.prototype.slice.call(all_textareas)
    var index = all_textareas.indexOf(textarea)
    var all_textarea_char_displays = document.getElementsByClassName('textarea-chars-count')
    var char_display = all_textarea_char_displays[index]
    
    var limit = char_display.innerHTML.split('/')[1]
    char_display.innerHTML = `${textarea.value.length} / ${limit}`
}

function remove_tag_param() {
    var newURL = location.href.split("?")[0];
    window.history.pushState('object', document.title, newURL);
    location.reload()
}

function all_inputs_blank(form) {
    var inputs = []
    inputs.push(...form.getElementsByTagName('input'))
    inputs.push(...form.getElementsByTagName('textarea'))

    for (let i = 0; i < inputs.length; i ++) {
        if (inputs[i].value != '' && inputs[i].name != 'csrfmiddlewaretoken') {
            return false
        }
    }
    return true
}

function search_suggestions() {
    var input = document.getElementById('tags-search')
    var tags = JSON.parse(document.getElementById('tags-list').textContent)
    var search_suggestions_container = document.getElementById('search-suggestions-container')
    const max_search_suggestions = JSON.parse(document.getElementById('max-search-suggestions').textContent)

    // clear search suggestions container before each oninput call
    for (let i = max_search_suggestions; i >= 0; i --) {
        if (search_suggestions_container.childNodes[i] != undefined) {
            search_suggestions_container.removeChild(search_suggestions_container.lastChild)
        } 
    }
    search_suggestions_container.style.padding = '0'
    search_suggestions_container.style.display = 'none'
    
    // create new containers for matched tags
    var matches = 0 
    for (let i = 0; i < tags.length; i ++ ) {
        if (tags[i].slice(0, input.value.length) == input.value.toLowerCase() && input.value != '') {
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
}

function is_textarea_maxlength_valid(textarea) {
    var maxlength = textarea.getAttribute('maxlength_value')
    if (textarea.value.length > maxlength) {
        textarea.value = textarea.value.slice(0, maxlength)
    }
}

function validate_post_create_input(form) {
    var inputs = []
    var textareas = form.getElementsByTagName('textarea')
    inputs.push(...form.getElementsByTagName('input'))
    inputs.push(...textareas)

    var error_msg = ''
    var submit_button = document.getElementById('submit-post')
    var error_msg_tag = document.getElementById('create-post-error-msg')
    var created_tags = document.getElementById(
        'created-tags'
    ).getElementsByTagName('button')
    var tags_input = document.getElementById('tags-input')

    for (let i = 0; i < inputs.length; i ++) {
        if (
            (inputs[i].required && inputs[i].value.length < 1 && inputs[i].id != 'tags-input') 
            || created_tags.length < 1
        ) {
            error_msg = 'Please fill in all required fields (*)'
        }
        if (created_tags.length >= 5) {
            tags_input.disabled = true
            tags_input.placeholder = 'Maximum of 5 tags. Click tags to remove them'
        } else {
            tags_input.disabled = false
            tags_input.placeholder = "Seperate tags with commas, eg : 'sport,'"
        }
    }
    error_msg_tag.innerHTML = error_msg
    if (error_msg == '') {
        submit_button.disabled = false
    } else {
        submit_button.disabled = true
    }
}

function set_confirm_refresh() {
    localStorage.setItem('confirm_refresh', false)
}

function show_remove_image_button(option) {
    document.getElementById(`remove-image-${option}-button`).style.display = 'block'
}

function click_file_input(option) {
    document.getElementById(`image-${option}-input`).click()
}

function change_element_display(element, display) {
    document.getElementById(element).style.display = display
} 

function remove_element_attribute(element, attribute) {
    document.getElementById(element).removeAttribute(attribute) 
}

function style_textareas_when_scroll_bar_visible() {
    var textareas = document.getElementsByTagName('textarea')
    for (let i = 0; i < textareas.length; i ++) {
        if (textareas[i].hasScrollBar()) {
            textareas[i].style.borderRadius = '0'
        }
    }
}

function change_element_value(option) {
    var hidden_input = document.getElementById(`remove_image_${option}`)
    hidden_input.value = 'REMOVE'
}