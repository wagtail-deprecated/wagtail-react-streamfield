function createSnippetChooser(id, modelString) {
    var chooserElement = $('#' + id + '-chooser');
    var docTitle = chooserElement.find('.title');
    var input = $('#' + id);
    var editLink = chooserElement.find('.edit-link');

    if (window.chooserUrls.snippetChooser) {
      var chooserUrl = window.chooserUrls.snippetChooser;
    } else {
      var chooserUrl = chooserElement.data('chooserUrl');
    }

    function snippetChosen(snippetData, initial) {
        if (!initial) {
            input.val(snippetData.id);
        }
        docTitle.text(snippetData.string);
        chooserElement.removeClass('blank');
        editLink.attr('href', snippetData.edit_link);
    }

    $('.action-choose', chooserElement).on('click', function() {
        ModalWorkflow({
            url: chooserUrl + modelString + '/',
            onload: SNIPPET_CHOOSER_MODAL_ONLOAD_HANDLERS,
            responses: {
                snippetChosen: snippetChosen,
            }
        });
    });

    $('.action-clear', chooserElement).on('click', function() {
        input.val('');
        chooserElement.addClass('blank');
    });

    if (input.val()) {
        $.ajax(chooserUrl + modelString + '/'
               + encodeURIComponent(input.val()) + '/')
            .done(function (data) {
                snippetChosen(data.result, true);
            });
    }
}
