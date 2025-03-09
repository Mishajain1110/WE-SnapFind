/* Make datetime picker use Font Awesome 5 */
$.fn.datetimepicker.Constructor.Default = $.extend({}, $.fn.datetimepicker.Constructor.Default, {
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

$(document).ready(function () {
    // Initialize datetime picker
    $('#datetimepicker').datetimepicker({
        locale: 'th',
        format: 'L',
        useCurrent: false,
    });

    // Initialize filter values
    let search_title = '';
    let search_location = '';
    let search_assetType = -1;
    let search_date = '';
    // let search_type ="lost";
    let search_is_active = -1;
    let isFirstLoad = true; // Track first API call

    // Initialize Swiper
    let swiper = new Swiper('.swiper-container', {
        slidesPerView: 3,
        spaceBetween: 20,
        loop: false,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        breakpoints: {
            1024: { slidesPerView: 3 },
            768: { slidesPerView: 2 },
            480: { slidesPerView: 1 }
        }
    });

    // Fetch posts and initialize the page
    initialize();

    // Event listener for Filter button
    $('#filterButton').on('click', function () {
        search_title = $('#title').val();
        search_location = $('#location').val();
        search_assetType = $('#assetType').val();
        // search_type = $('#type').val();
        search_is_active = $('#is_active').val();
        initialize();
    });
    let search_type = 'lost';
    // Function to fetch and display posts
    function initialize() {
        let search_type = 'lost';
        // console.log('Initializing with:', {
        //     search_title,
        //     search_location,
        //     search_assetType,
        //     search_date,
        //     search_type,  // Ensure this is always 'lost'
        //     search_is_active
        // });
        console.log('search_type:', search_type);

        axios.get('/post_api/', {
            params: {
                search_title, search_location, search_assetType, search_date, search_type:'lost', search_is_active,
            },
        })
        .then(function (response) {
            const [posts, assetTypes] = response.data;

            // Populate asset type dropdown on first load
            if (isFirstLoad) {
                $('#assetType').html('<option value="-1">All Item Types</option>');
                assetTypes.forEach(asset => {
                    $('#assetType').append(`<option value="${asset.id}">${asset.name}</option>`);
                });
                isFirstLoad = false;
            }

            // Clear existing slides
            $('.swiper-wrapper').empty();

            if (posts.length === 0) {
                $('.swiper-wrapper').html(`
                    <div class="swiper-slide text-center">
                        <div class='col-lg-12 jumbotron text-center border border-dark'>
                            <img src="/static/images/post.png" width='15%' class='mb-5'>
                            <h4>No Posts</h4>
                        </div>
                    </div>
                `);
            } else {
                posts.forEach(post => {
                    const imageUrl = post.pictures.length > 0 ? post.pictures[0].picture : '/static/images/post_default.gif';
                    const postHtml = `
                        <div class="swiper-slide">
                            <div class="card h-100 w-100 text-dark mycard">
                                <a href="/detail/${post.id}/">
                                    <div class="wrapper">
                                        <img class="card-img-top" src="${imageUrl}" alt="${post.title}">
                                    </div>
                                    <div class="card-body">
                                        <h5 class="card-title"><b>${post.title}</b></h5>
                                        <p class="card-text"><small>${post.location}</small></p>
                                        <p class="card-text">
                                            <span class="badge badge-pill ${post.type === 'found' ? 'badge-success' : 'badge-danger'}">
                                                ${post.type === 'found' ? 'Found' : 'Lost'}
                                            </span>
                                        </p>
                                    </div>
                                </a>
                            </div>
                        </div>
                    `;
                    $('.swiper-wrapper').append(postHtml);
                });
            }

            // Update Swiper after adding new slides
            swiper.update();
        })
        .catch(function (error) {
            console.error('Error fetching posts:', error);
        });
    }

    // Search Filters
    $('#search_title').on('keyup', function() { search_title = $(this).val(); initialize(); });
    $('#search_location').on('keyup', function() { search_location = $(this).val(); initialize(); });
    $('#search_date').on('change', function() { search_date = $(this).val(); initialize(); });
    // $('#search_type').on('change', function() { search_type = $(this).val(); initialize(); });
    $('#search_is_active').on('change', function() { search_is_active = $(this).val(); initialize(); });
    $('#assetType').on('change', function() { search_assetType = $(this).val(); initialize(); });

    // Clear Date Functionality
    function clearDate() {
        $('#datetimepicker').datetimepicker('clear');
        search_date = '';
        initialize();
    }

    // Reset Search
    function resetSearch() {
        search_title = '';
        search_location = '';
        search_assetType = -1;
        search_date = '';
        // search_type = -1;
        search_is_active = -1;
        initialize();
    }
});