document.addEventListener('DOMContentLoaded', () => {
    
    // Login form logic
    const loginForm = document.querySelector('form[action="/login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            const userField = document.getElementById('username');
            const passField = document.getElementById('password');

            if (userField.value === "" || passField.value === "") {
                event.preventDefault(); 
                alert("ACCESS DENIED: Credentials Required.");
            }
        });
    }

    // Capsule form logic
    const capsuleForm = document.querySelector('form[action="/submit_time_capsule"]');
    if (capsuleForm) {
        capsuleForm.addEventListener('submit', function(event) {
            const dateField = document.getElementById('open-date');
            
            // Create Date objects for comparison
            const selectedDate = new Date(dateField.value);
            const now = new Date();

            if (!dateField.value) {
                event.preventDefault();
                alert("ERROR: Time coordinate required.");
                return;
            }

            if (selectedDate <= now) {
                event.preventDefault();
                alert("ERROR: Temporal paradox detected. Destination time must be in the future.");
            } else {
                if(!confirm("Lock this capsule? It cannot be opened until " + selectedDate.toLocaleString())) {
                    event.preventDefault();
                }
            }
        });
    }
});