function remove_placeholder_text(element) {
    element.placeholder = ''
}

function return_tags() {
    var tags_container = document.getElementById('created-tags').childNodes
    var tags_input = document.getElementById('tags-input')
    var tags_string = ''

    for (let i = 0; i < tags_container.length; i ++) {
        tags_string += tags_container[i].innerHTML
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
        input_width = `${(input_width - tags_width) * 2}%`

        element.style.width = input_width

    }
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
    
    // create new containers for matched tags
    var matches = 0 
    for (let i = 0; i < tags.length; i ++ ) {
        if (tags[i].includes(input.value.toLowerCase()) && input.value != '') {
            var node = document.createElement('div')
            node.innerHTML = tags[i]
            search_suggestions_container.appendChild(node)
            matches += 1
        }
    }



}