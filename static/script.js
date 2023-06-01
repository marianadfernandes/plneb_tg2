$(document).ready(function () {
    $('#example').DataTable();
});


function deleteTerm(designation){ 
    $.ajax("/term/" + designation, {
        type:"DELETE",
        success: function(data) {
            window.location.href = '/terms';
        },
        error: function(error) {
            console.error('Error:', error);
        }
    })

}


function deleteTerm_woman(designation){ 
    $.ajax("/term-woman/" + designation, {
        type:"DELETE",
        success: function(data) {
            window.location.href = '/terms-woman';
        },
        error: function(error) {
            console.error('Error:', error);
        }
    })

}


