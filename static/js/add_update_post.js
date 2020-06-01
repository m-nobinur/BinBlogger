rangy.init();

var HighlighterButton = MediumEditor.extensions.button.extend({
  name: "highlighter",
  tagNames: ["mark"],
  contentDefault: "<b>H</b>",
  contentFA: '<i class="fa fa-paint-brush"></i>',
  aria: "Highlight",
  action: "highlight",

  init: function () {
    MediumEditor.extensions.button.prototype.init.call(this);

    this.classApplier = rangy.createClassApplier("highlight", {
      elementTagName: "mark",
      normalize: true,
    });
  },

  handleClick: function (event) {
    this.classApplier.toggleSelection();
    this.base.checkContentChanged();
  },
});
var editor = new MediumEditor("#id_content", {
  toolbar: {
    buttons: [
      "h1",
      "h3",
      "bold",
      "italic",
      "anchor",
      "orderedlist",
      "unorderedlist",
      "highlighter",
      "quote",
      "image",
      "justifyLeft",
      "justifyCenter",
      "justifyRight",
      "pre",
      "outdent",
      "indent",
      {
        name: "html",
        contentDefault: "<i>Html</i>",
        contentFA: '<i class="fa fa-html5"></i>',
      },
    ],
  },
  buttonLabels: "fontawesome",
  extensions: {
    highlighter: new HighlighterButton(),
  },
  placeholder: false,
});

$(document).ready(function () {
  // Prepare the preview for profile picture
  $("#id_post_thumbnail").change(function () {
    readURL(this);
  });
});
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $("#wizardPicturePreview").attr("src", e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
}
$("pre").wrapInner('<code class="language-python"></code>');

$(".selectmultiple").attr({
  "data-max-options": "3",
  "data-live-search": true,
  "data-width": "fit",
  "data-style": "btn-outline-info",
  title: "Select categories...",
  "data-selected-text-format": "count > 3",
});
$("select").selectpicker();
