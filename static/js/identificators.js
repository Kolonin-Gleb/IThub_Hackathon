
var set_identificators = function(value, data) {
    let search = get('.search-btn');
    search.style.display = 'flex';

    let container = get('.identificators-container');
    container.style.display = 'flex';


    for (let i = 1; i <= 7; i++) {
        let block = get(`#ident-${i}`);
        let block_data = data[value][i];
        block.innerHTML = ''
        Array.from(block_data).forEach(cur_data => {
            let cur_data_origin = cur_data;
            cur_data = cur_data.replace('<', '##(').replace('>', ')##');
            block.innerHTML += `
            <label>
                <input type="checkbox" hidden name="ident-${i}" value='${cur_data}'>
                <span class="content">${cur_data_origin}</span>
            </label>
            `;
        });
    }
}

var add_identificators = function(value) {
    $.ajax({
        url: '/get_identificator_data',
        type: 'POST',
        dataType : 'json',
        success: function (data) {
            set_identificators(value, data);
        },
        error: function(jqxhr, status, errorMsg) {
            alert('Server error!');
        }
    });
}
