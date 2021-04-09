it('calls ajax post on form submit button click for genres and video type', function() {
    view.render();
    var form = $('#genre-form');
    var submitCallback = jasmine.createSpy().andReturn(false);
    form.submit(submitCallback);
  
    $('#export_images_xml_button').click();
    const formData = {'Genres': 28, 'Type': 'Movies'}
    expect(form.attr('action')).toEqual('/export');
    expect($('#genre-filter-submit').attr('value')).toEqual(data);
    expect(submitCallback).toHaveBeenCalled();
  });