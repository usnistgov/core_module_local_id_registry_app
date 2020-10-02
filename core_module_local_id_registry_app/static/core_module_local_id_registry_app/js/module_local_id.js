const moduleLocalIdClass = ".mod-local-id";

// Send module data for saving
let saveLocalIdModuleData = function(event) {
    event.stopPropagation();

    let $module = $(this).parents(".module");
    let moduleLocalIdData = {
        "data": [
            $module.find("input.pid-host-url").val(),
            $module.find("select.pid-prefix").val(),
            $module.find(".mod_input input").val()
        ].join("/")
    };

    saveModuleData($module, moduleLocalIdData);
};

$(document).ready(function() {
    // Register events on module widgets once the page is loaded.
    let $body = $("body");
    $body.on("blur", moduleLocalIdClass + " input[type='text']", saveLocalIdModuleData);
    $body.on("change", moduleLocalIdClass + " select", saveLocalIdModuleData);

    // Fix hostname hidden if input is not wide enough.
    let $pidHostURLInput = $("input.pid-host-url");
    $pidHostURLInput.css("width",(($pidHostURLInput.val().length + 1) * 10) + "px");
});
