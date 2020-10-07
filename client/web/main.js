window.addEventListener('load', function () {
    input_key = document.getElementById("input_key");
    di_room_code = document.getElementById("di_room_code");
    di_current_state = document.getElementById("di_current_state");
    di_bot_server = document.getElementById("di_bot_server");
    di_current_key = document.getElementById("di_current_key");
    di_delay_after_meeting = document.getElementById("di_delay_after_meeting");
    di_repo_link = document.getElementById("di_repo_link");
    txt_output = document.getElementById("txt_output");

    clamp = function(num, min, max) {
        return Math.min(Math.max(num, min), max);
    };

    eel.expose(add_output);
    function add_output(text) {
        txt_output.value += text;
        txt_output.scrollTop = txt_output.scrollHeight;
    };

    eel.expose(output_remove_lines);
    function output_remove_lines(lines) {
        txt_output.value = txt_output.value.split("\n").slice(0, -1 - lines).join("\n") + "\n";
    };

    eel.expose(set_room_code);
    function set_room_code(text) {
        di_room_code.textContent = text
    }

    eel.expose(set_current_state);
    function set_current_state(text) {
        di_current_state.textContent = text
    }

    eel.expose(set_bot_server);
    function set_bot_server(text) {
        di_bot_server.textContent = text
    }

    eel.expose(set_current_key);
    function set_current_key(text) {
        di_current_key.textContent = text
    }

    input_key.addEventListener("input", function (evt) {
        this.value = this.value.replaceAll(" ", "");
        eel.update_key(this.value);
    });

    di_delay_after_meeting.addEventListener("input", function (evt) {
        this.value = this.value.replace(/\D/g,'');
        num = clamp(parseInt(this.value), 0, 10);
        if (isNaN(num)) {
            num = 0;
        } else {
            this.value = num.toString();
        }
        eel.update_mute_delay_meeting(num);
    });

    di_repo_link.addEventListener("click", function (evt) {
        eel.open_repo();
    });
});