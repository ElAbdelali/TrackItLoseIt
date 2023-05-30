document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    
    var formData = new FormData(this);
    var xhr = new XMLHttpRequest();
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.redirect) {
                    window.location.href = response.redirect;
                } else if (response.message) {
                    document.getElementById('status-message').innerText = response.message;
                }
            }
        }
    };
    
    xhr.open(this.method, this.action, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.send(formData);
});
