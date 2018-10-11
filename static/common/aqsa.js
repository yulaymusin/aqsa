$(document).ready(function() {
/* Instead of this JS, using the templatetags.
  $('form').find('.form-group').find('input').addClass('form-control');
  $('form').find('.form-group').find('select').addClass('form-control');
*/
/* <FIX for chosen-select for show the "required" message from browser. Source: https://github.com/harvesthq/chosen/issues/515#issuecomment-403738593 */
  /* currency required making new wallet and new "balance_of_category" report */
  var current_uri = window.location.pathname;
  if(current_uri.indexOf('/wallet_tag_etc/wallet/new')+1 || current_uri.indexOf('/report/balance_of_category_create')+1){
    $('select[name="currency"]').parent().addClass('form__select');
    $('select[name="currency"]').addClass('chosen');
  }
/* </FIX for chosen-select for show the "required" message from browser. Source: https://github.com/harvesthq/chosen/issues/515#issuecomment-403738593 */
});