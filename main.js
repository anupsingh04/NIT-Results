// Main JavaScript file for the NIT Hamirpur Results App

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            const rollNumberInput = document.getElementById('roll_number');
            const rollNumber = rollNumberInput.value.trim();
            
            // Basic validation pattern for roll numbers (e.g., 22BEC025)
            const rollNumberPattern = /^\d{2}[A-Z]{2,3}\d{3}$/;
            
            if (!rollNumberPattern.test(rollNumber)) {
                event.preventDefault();
                
                // Create or update error message
                let errorDiv = document.querySelector('.roll-number-error');
                if (!errorDiv) {
                    errorDiv = document.createElement('div');
                    errorDiv.className = 'roll-number-error alert alert-danger mt-2';
                    rollNumberInput.parentNode.appendChild(errorDiv);
                }
                
                errorDiv.textContent = 'Please enter a valid roll number (e.g., 22BEC025)';
                
                // Focus on the input field
                rollNumberInput.focus();
            }
        });
    }
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Print functionality
    const printButton = document.querySelector('.btn-print');
    if (printButton) {
        printButton.addEventListener('click', function() {
            window.print();
        });
    }
});
