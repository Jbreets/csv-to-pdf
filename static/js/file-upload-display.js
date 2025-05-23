document.addEventListener("DOMContentLoaded", () => {
    const parqFileInput = document.getElementById('parq_file');
    const emailsFileInput = document.getElementById('emails');
    const csvFileInput = document.getElementById('csv_pdf');

    if (parqFileInput) {
        parqFileInput.addEventListener('change', function () {
            const fileName = this.files[0] ? this.files[0].name : 'No file chosen';
            document.getElementById('parq_filename').textContent = fileName;
        });
    }

    if (emailsFileInput) {
        emailsFileInput.addEventListener('change', function () {
            const fileName = this.files[0] ? this.files[0].name : 'No file chosen';
            document.getElementById('emails_filename').textContent = fileName;
        });
    }

    if (csvFileInput) {
        csvFileInput.addEventListener('change', function () {
            const fileName = this.files[0] ? this.files[0].name : 'No file chosen';
            document.getElementById('csv_filename').textContent = fileName;
        })
    }

});