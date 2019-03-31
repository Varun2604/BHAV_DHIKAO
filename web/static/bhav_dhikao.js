const TEMPLATES = {
    'table_rows': Handlebars.compile(document.querySelector('script#table-rows').innerHTML),
    'date_list': Handlebars.compile(document.querySelector('script#date-list').innerHTML)
};

(function () {
    function loadDataFor(date, search_str, regex_search) {
        var query_params = {};
        if (search_str) {
            query_params = {
                date: date,
                search_str: search_str,
                regex_search: regex_search
            };
        } else {
            query_params = {
                date: date,
                count: 10
            };
        }
        get_ajax('data', query_params).done(function (data) {
            document.querySelector('.table-row .table-body').innerHTML = TEMPLATES.table_rows({rows: JSON.parse(data)});
        }).fail(function (jqXHR, textStatus, errorThrown) {
            document.querySelector('.table-row .table-body').innerHTML = TEMPLATES.table_rows({rows: []});
        });
    }

    function onDateClick(event) {
        document.querySelector('.date-list .scrollable-div .selectable-date.active').classList.remove('active');
        event.target.classList.add('active');
        loadDataFor(event.target.value)
    }

    // fill the date list
    get_ajax('available_dates', {}).done(function (data) {

        var dates = [];
        for (var date of JSON.parse(data)) {
            var [dd,mm,yyyy] = date.split('-');
            var d = new Date(dd, mm, yyyy);
            dates.push({
                value: date,
                display_value: d.toDateString()
            });
        }
        dates[0].active = true;
        loadDataFor(dates[0].value);
        var scrollable_div = document.querySelector('.date-list .scrollable-div');
        scrollable_div.innerHTML = TEMPLATES.date_list({dates: dates});
        scrollable_div.querySelectorAll('.selectable-date').forEach(function (x) {
            x.onclick = onDateClick;
        });

    }).fail(function (jqXHR, textStatus, errorThrown) {
        var scrollable_div = document.querySelector('.date-list .scrollable-div');
        scrollable_div.innerHTML = TEMPLATES.date_list({dates: []});
        scrollable_div.querySelectorAll('.selectable-date').forEach(function (x) {
            x.onclick = onDateClick;
        });
    });

    //set events to the date list

    //set event to the search element
    document.querySelector('.search-bar .search').onclick = function (event) {
        loadDataFor(document.querySelector('.date-list .scrollable-div .selectable-date.active').value, document.querySelector('.search-bar input').value, false);
    };
    document.querySelector('.search-bar .regex-search').onclick = function (event) {
        loadDataFor(document.querySelector('.date-list .scrollable-div .selectable-date.active').value, document.querySelector('.search-bar input').value, true);
    };
})();

function get_ajax(entity, data) {
    return $.ajax({
        url: '/api/' + entity,
        method: 'GET',
        data: data
    });
}