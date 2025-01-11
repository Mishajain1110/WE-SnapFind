/* Make datetime picker use Font Awesome 5 */
$.fn.datetimepicker.Constructor.Default = $.extend({}, $.fn.datetimepicker.Constructor.Default,{
    icons: {
        time: 'fas fa-clock',
        date: 'fas fa-calendar-alt',
        up: 'fas fa-arrow-up',
        down: 'fas fa-arrow-down',
        previous: 'fas fa-chevron-left',
        next: 'fas fa-chevron-right',
        today: 'fas fa-calendar-check-o',
        clear: 'fas fa-trash',
        close: 'fas fa-times'
    }
});

/* initial datetime picker */
$('#datetimepicker').datetimepicker({
    locale: 'th',
    format: 'L',
    useCurrent: false
});


var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
search_title = ''
search_location = ''
search_assetType = -1
search_date = ''
search_type = -1
search_is_active = -1
loaded = false
function initialize(){
    axios.get('/post_api/' +
        '?search_title=' + search_title +
        '&search_location=' + search_location +
        '&search_assetType=' + search_assetType +
        '&search_date=' + search_date +
        '&search_type=' + search_type +
        '&search_is_active=' + search_is_active
    ).then(function (response) {
        // handle success
        data = response.data

        posts = data[0]
        assetTypes = data[1]

        // wipe page
        $('#all_post').html('')
        $('#assetType').html('')

        createAssetTypeChoice(assetTypes)

        for (i = 0; i < posts.length; i++){
            if (posts[i].pictures.length >= 1){
                url =  posts[i].pictures[0].picture
            }
            else{
                url = null;
            }
            createCard(posts[i].id, url, posts[i].title, posts[i].desc, posts[i].type,
                posts[i].assetType, posts[i].location, posts[i].date_time,
                posts[i].contact1, posts[i].contact2, posts[i].user, posts[i].is_active)
        }

        if (posts.length == 0){ // if not have any posts
            /*
            <div class='col-lg-12 jumbotron text-center border border-dark'>
                <img src="{% static 'images/post.png' %}" width='15%' class='mb-5'>
                <h4>No posts</h4>
            </div>
            */
            let div = document.createElement('div')
            div.setAttribute('class', 'col-lg-12 jumbotron text-center border border-dark')

            let img = document.createElement('img')
            img.setAttribute('src', '/static/images/post.png')
            img.setAttribute('width', '15%')
            img.setAttribute('class', 'mb-5')

            let h4 = document.createElement('h4')
            h4.innerText = 'No posts'

            div.append(img)
            div.append(h4)

            document.getElementById('all_post').append(div)
        }
    })
    .catch(function (error) {
        // handle error
        console.log(error);
    })
}

function createCard(id, url, title, desc, type, assetType, location, date_time, contact1, contact2, user, is_active){
    let a = document.createElement('a')
    a.setAttribute('class', 'col-lg-3 my-3 text-decoration-none')
    a.setAttribute('href', '/detail/' + id + '/')

    let card = document.createElement('div')
    card.setAttribute('class', 'card h-100 w-100 text-dark mycard')

    card.append(createCardWrapper(url))
    card.append(createCardBody(title, desc, assetType, location, date_time))
    card.append(createCardText(type, is_active))
    card.append(createCardFooter(contact1, contact2, user))

    a.append(card)

    document.getElementById('all_post').append(a)
}

function createCardWrapper(url){
    /*
    <div class="wrapper">
        {% if post.postpicture_set.all|length == 0 %}
            <img class="card-img-top" src="{% static 'images/post_default.gif' %}">
        {% else %}
            <img class="card-img-top" src="{{ post.postpicture_set.all.0.picture.url }}">
        {% endif %}
    </div>
    */
    let div = document.createElement('div')
    div.setAttribute('class', 'wrapper')

    let img = document.createElement('img')
    if (url === null){
        img.setAttribute('src', '/static/images/post_default.gif')
    }
    else{
        img.setAttribute('src', url)
    }
    div.append(img)

    return div
}

function createCardBody(title, desc, assetType, location, date_time){

    let div = document.createElement('div')
    div.setAttribute('class', 'card-body')

    let h5 = document.createElement('h5')
    h5.setAttribute('class', 'card-title')
    h5.append(createBoldText(truncatechars(title, 20)))

    let cardtext = document.createElement('div')
    cardtext.setAttribute('class', 'card-text')

    let p1 = document.createElement('p')
    p1.innerText = truncatechars(desc, 15)

    let p2 = document.createElement('p')
    p2.setAttribute('class', 'm-0')
    let small = document.createElement('small')
    small.append(createBoldText('Item type: '))
    small.append(assetType)
    p2.append(small)

    let p3 = document.createElement('p')
    p3.setAttribute('class', 'm-0')
    small = document.createElement('small')
    small.append(createBoldText('Location: '))
    small.append(location)
    p3.append(small)

    let p4 = document.createElement('p')
    p4.setAttribute('class', 'm-0')

    let datetime = new Date(date_time)
    datetime = ((datetime.getDate() < 10 ? '0' : '') + datetime.getDate()) + '/' + ((datetime.getMonth() + 1 < 10 ? '0' : '') + (datetime.getMonth() + 1)) + '/' +
                 datetime.getFullYear() + ' ' + ((datetime.getHours() < 10 ? '0' : '') + datetime.getHours()) + ':' + ((datetime.getMinutes() < 10 ? '0' : '') + datetime.getMinutes())

    p4.innerHTML = '<small> <b>Date and Time: </b>' + datetime + '</small>'

    // append
    cardtext.append(p1)
    cardtext.append(p2)
    cardtext.append(p3)
    cardtext.append(p4)

    div.append(h5)
    div.append(cardtext)

    return div
}

function createCardText(type, is_active){
    /*
    <div class="container mb-3 ml-1">
        <p class="card-text">
            <span class="badge badge-pill badge-success text-light">Found Lost Item</span>
        </p>
    </div>
    */

    let div = document.createElement('div')
    div.setAttribute('class', 'container mb-3 ml-1')

    let p = document.createElement('p')
    p.setAttribute('class', 'card-text')
    if (type == 'found'){
        p.innerHTML = ' <span class="badge badge-pill badge-success text-light"> Found Lost Item </span>'
    }
    else{
        p.innerHTML = ' <span class="badge badge-pill badge-danger text-light"> Looking for Item </span>'
    }


    if (!is_active){
        p.innerHTML += ' <span class="badge badge-pill badge-dark text-light">Closed</span>'
    }


    div.append(p)

    return div
}

function createCardFooter(contact1, contact2, user){
    /*
    <div class="card-footer">
        <small class="text-muted">
            <b>Contact number: </b> <span id='contact1'> {{ post.contact1 }} </span>
            <br>
            <b>Email: </b> <span id='contact2'> {{ post.contact2 }} </span>
            <br>
            <b>By: </b> {{ post.user.username }}
        </small>
    </div>
    */

    let div = document.createElement('div')
    div.setAttribute('class', 'card-footer')

    let small = document.createElement('small')
    small.setAttribute('class', 'text-muted')

    let span1 = document.createElement('span')
    span1.append(createBoldText('Contact number: '))
    span1.append(contact1)
    span1.append(document.createElement('br'))

    let span2 = document.createElement('span')
    span2.append(createBoldText('Email: '))
    span2.append(contact2)
    span2.append(document.createElement('br'))

    let span3 = document.createElement('span')
    span3.append(createBoldText('By: '))
    if (user){
        span3.append(user)
    }
    else{
        span3.append('General User')
    }
    span3.append(document.createElement('br'))

    small.append(span1)
    small.append(span2)
    small.append(span3)

    div.append(small)

    return div
}

function createBoldText(text){
    let b = document.createElement('b')
    b.innerText = text
    return b
}

function truncatechars(str, len){
    if (str.length > len){
        return str.substring(0, len) + '...'
    }
    else{
        return str
    }
}

function createAssetTypeChoice(assetTypes){
    let option = document.createElement('option')
    option.setAttribute('value', -1)
    option.innerText = 'All Item Types'
    document.getElementById('assetType').append(option)
    for (let i = 0; i < assetTypes.length; i++){
        let option = document.createElement('option')
        option.setAttribute('value', assetTypes[i].id)
        option.innerText = assetTypes[i].name
        document.getElementById('assetType').append(option)
    }
}

function resetSearch(){
    search_title = ''
    search_location = ''
    search_assetType = -1
    search_date = ''
    search_type = -1
    search_is_active = -1
    initialize()
}

$('#search_title').on('keyup', function() {
    search_title = $(this).val()
    initialize()
})

$('#search_location').on('keyup', function() {
    search_location = $(this).val()
    initialize()
})

$('#search_date').on('change', function() {
    search_date = $(this).val()
    initialize()
})

$('#search_type').on('change', function() {
    search_type = $(this).val()
    initialize()
})

$('#search_is_active').on('change', function() {
    search_is_active = $(this).val()
    initialize()
})

$('#assetType').on('change', function() {
    search_assetType = $(this).val()
    initialize()
})

$(document).ready(function(){
    initialize()
})
