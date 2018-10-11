var config = {
  '.chosen-select'           : { allow_single_deselect: true },
}
for (var selector in config) {
  $(selector).chosen(config[selector]);
}
