document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('import_csv').onchange = function() {
        if (this.files.length > 0) {
            document.getElementById('import_from_csv').submit();
        }

    };
});

function openExportModal() {
    const modal = document.getElementById("modal");
    const noBtn = document.getElementById("no-btn");
    const form = document.getElementById("export-form");
    //const yes-a = document.getElementById("yes-a");
    //console.log(yes-a);

    modal.style.display = "flex";

    noBtn.onclick = function () {
        modal.style.display = "none";
    };

    form.addEventListener('submit', function(e) {
        modal.style.display = "none";
    });


}

function openSendList() {
    const modal = document.getElementById("modal_1");
    const noBtn = document.getElementById("no-btn-1");
    const form = document.getElementById("sendlist_form");

    modal.style.display = "flex";

    noBtn.onclick = function () {
        modal.style.display = "none";
    };

    form.addEventListener('submit', function(e) {
        modal.style.display = "none";
    });
}


function delete_listener() {

    const modal = document.getElementById("modal");

    const message = document.getElementById("modal-message");

    const yesA = document.getElementById("yes-a");

    const noBtn = document.getElementById("no-btn");

    message.innerText =
        "Вы уверены, что хотите удалить запись?";

     modal.style.display = "flex";
    yesA.onclick = function () {
        document.getElementById("delete_form").submit();
    };


    noBtn.onclick = function () {
        modal.style.display = "none";
    };
}

function change_listener() {

    const modal = document.getElementById("modal");

    const message = document.getElementById("modal-message");

    const yesA = document.getElementById("yes-a");

    const noBtn = document.getElementById("no-btn");

    message.innerText = "Вы уверены, что хотите внести изменения в данные слушателя?";

    yesA.onclick = function () {
        document.getElementById("change_form").submit();
    };

    modal.style.display = "flex";

    noBtn.onclick = function () {
        modal.style.display = "none";
    };
}

function send_mail() {

    const modal = document.getElementById("modal");

    const message = document.getElementById("modal-message");

    const yesA = document.getElementById("yes-a");

    const noBtn = document.getElementById("no-btn");

    message.innerText =
        "Вы уверены, что хотите отправить сообщение?";

     modal.style.display = "flex";
    yesA.onclick = function () {
        document.getElementById("send_mail_form").submit();
    };


    noBtn.onclick = function () {
        modal.style.display = "none";
    };
}

