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


function formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    const formattedDate = `${year}-${month}-${day}T${hours}:${minutes}`;

    return formattedDate;
}

document.addEventListener('DOMContentLoaded', function() {
    const taskId = document.querySelector('meta[name="task-id"]').getAttribute('content');
    if (!taskId) {
        return;
    }
    const csrfToken = getCookie('csrftoken');
    
    fetch(`/api/tasks/${taskId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('taskId').value = data.id;
        document.getElementById('id_user_email').value = data.user_email;
        document.getElementById('id_task').value = data.task;
        document.getElementById('id_due_by').value = formatDateTime(data.due_by);
        document.getElementById('id_priority').value = data.priority;
        document.getElementById('id_is_urgent').checked = data.is_urgent;
    })
    .catch(error => console.error('Error fetching task:', error));
});