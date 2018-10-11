$(document).ready(function() {
/* <for tables (list of transactions, new set, list the edit mode...) */
  $('tbody').scroll(function(e) { // detect a scroll event on the tbody
    $('thead').css("left", -$("tbody").scrollLeft()); // fix the thead relative to the body scrolling
    $('thead th:nth-child(1)').css("left", $("tbody").scrollLeft()); // fix the first cell of the header
    $('tbody td:nth-child(1)').css("left", $("tbody").scrollLeft()); // fix the first column of tdbody
  });

  /* <width of every column in thead is the same with width of corresponding columns in tbody */
  var td_widths = [];
  var tbody_row = $('.transaction_list_table').children('table').children('tbody').children('tr:nth-child(1)').children('td');
  $(tbody_row).each(function(i, elem) {
    td_widths.push($(elem).outerWidth());
    $(elem).css({'width': td_widths[i]+'px'});
  });
  var thead_row = $('.transaction_list_table').children('table').children('thead').children('tr:first').children('th');
  $(thead_row).each(function(i, elem) {
    $(elem).css({'min-width': td_widths[i]+'px'});
  });
  /* </width of every column in thead is the same with width of corresponding columns in tbody */

  /* <height of every cell in first column of tbody is the same with height of another columns */
  var tbody_first_col = $('.transaction_list_table').children('table').children('tbody').children('tr:nth-child(1)').children('td:nth-child(2)').outerHeight();
  var tbody_rows = $('.transaction_list_table').children('table').children('tbody').children('tr');
  $(tbody_rows).each(function(i, row) {
    $(row).children('td:nth-child(1)').css({'min-height': tbody_first_col});
  });
  /* <height of every cell in first column of tbody is the same with height of another columns */
/* </for tables (list of transactions, new set, list the edit mode...) */
});



/* <for URI: "list_the_edit_mode" */
function update_transaction(transaction_id){
  var form = $('#' + transaction_id);
  var form_data = form.serialize();
  var action = form.attr('action');
  $.ajax({
    type: 'POST',
    url: action,
    data: form_data,
    success: function(data) {
      var answer = JSON.parse(data);
      // console.log(answer['updated']);
      // console.log(answer['msg']);
      // console.log(answer['errors']);
      // console.log(answer['errors_in_fields']);

      var title = '<b>' + answer['msg'] + '</b>';
      if (answer['updated'] == 'yes') {
        var type = 'success';
        var timer = 1500;
        var message = '';
        // TODO: removeClass('has-error');
      }
      else if (answer['updated'] == 'no') {
        var type = 'danger';
        var timer = 4500;  // probably, user needs more time to read about errors

        /* <add to the message all errors of every field which contains any error */
        var message = '<ul>';
        $.each(answer['errors'], function(key, value){
          message = message + '<li><u>' + key + '</u>';
          message += '<ul>';
          $.each(value, function(err_index, err_value){
            message = message + '<li>' + err_value + '</li>';
          });
          message += '</ul>';
          message += '</li>';
        });
        message += '</ul>';
        /* </add to the message all errors of every field which contains any error */

        /* <add the error class to each form-group div, which child input/select contains an error */
        var field = null;
        var form_group = null;
        // console.log('____________________________')
        $.each(answer['errors_in_fields'], function(index, value){
          // console.log(index, value, transaction_id);
          field = $('[name="'+ value +'"][form="' + transaction_id +'"]');
          form_group = field.parent('.form-group');
          form_group.addClass('has-error');
        });
        /* </add the error class to each form-group div, which child input/select contains an error */
      }

      /* <notify user */
      $.notify({
        icon: "nc-icon nc-app",
        title: title,
        message: message
      }, {
        type: type,  // possible values: 'primary', 'info', 'warning', 'success', 'danger'
        timer: timer,
        placement: {
          from: 'bottom',
          align: 'left'
        },
        animate: {
          enter: 'animated fadeInDown',
          exit: 'animated fadeInDown'
        },
      });
      /* </notify user */
    },
    /* In normal situations user can't get 404, only if user trying to update foreign transaction. Let's just alert */
    error: function(xhr, str){
      if(xhr.status == 404) {
        alert('404 Not Found');
      }
      else {
        alert(xhr.status);
      }
    }
  });
}
/* <call the "update_transaction" function when user change a field (input, select, etc) */
$('.form-control').on('change', function() {
  /* let's check user on the "list_the_edit_mode" page or not,
     because ".form-control" elements exists on many other pages too */
  var current_uri = window.location.pathname;
  if(current_uri.indexOf('/transaction/list_the_edit_mode')+1){
    var id = $(this);
    var transaction_id = id.attr('form');
    /* check by id of form: user edit a transaction or change "paginate_by"  */
    if(transaction_id != 'paginate_by_form') {
      update_transaction(transaction_id);
    }
  }
});
/* </for URI: "list_the_edit_mode" */