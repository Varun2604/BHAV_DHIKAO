const TEMPLATES = {
    'table_rows': Handlebars.compile(document.querySelector('script#table-rows').innerHTML),
    'date-list': Handlebars.compile(document.querySelector('script#date-list').innerHTML),
};

(function () {

    // fill the page with first 10 rows initially
    get_ajax('data', {
        'count': 9,
        'date': '2019-03-27'
    }).done(function (data) {
        document.querySelector('.table-row .table-body').innerHTML = TEMPLATES.table_rows({rows: JSON.parse(data)});
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log(arguments)
    });

    //set events to the date list

    //set event to the search element
    document.querySelector('.search-bar button').onclick = function () {
        get_ajax('data', {
            'name': document.querySelector('.search-bar input').value,
            'date': '2019-03-27'
        }).done(function (data) {
            document.querySelector('.table-row .table-body').innerHTML = TEMPLATES.table_rows({rows: [JSON.parse(data)]});
        }).fail(function (jqXHR, textStatus, errorThrown) {
            document.querySelector('.table-row .table-body').innerHTML = TEMPLATES.table_rows({rows: []});
        });
    };
})();

function get_ajax(entity, data) {
    return $.ajax({
        url: '/api/' + entity,
        method: 'GET',
        data: data
    });
}