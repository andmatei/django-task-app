$(document).ready(function() {
    $('#taskForm').on('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way
        var formArray  = $(this).serializeArray(); // Serialize the form data
        var formData = {};
        $.each(formArray, function(index, field) {
            formData[field.name] = field.value;
        });
        console.debug('Form data:', formData);
        
        // Ensure checkbox is correctly added to formData
        formData['is_urgent'] = $('#is_urgent').is(':checked') ? true : false;

        var taskId = $('#taskId').val();
        var url = '/api/tasks';
        var method = 'POST';
        
        if (taskId) {
            console.debug('Task instance ID found, updating existing task');
            url = '/api/tasks/' + taskId;
            method = 'PUT';
        }

        var csrfToken = getCookie('csrftoken'); // Get CSRF token from the cookie


        $.ajax({
            url: url,
            type: method,
            data: JSON.stringify(formData),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken // Include the CSRF token in the headers
            },
            success: function(response) {
                // Handle the successful response here
                console.log('Form submitted successfully:', response);
                window.location.href = '/tasks/dashboard';
            },
            error: function(xhr, status, error) {
                // Handle the error response here
                console.error('Form submission failed:', error);
                alert('Error submitting form: ' + error);
            }
        });
    });
});


// Function to get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}