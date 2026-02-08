// Global variables
let currentBirthdayId = null;
let currentImageBase64 = null;

// Load birthdays on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTodayBirthdays();
    loadUpcomingBirthdays();
});

// Sign Out
document.getElementById('signout-btn').addEventListener('click', async () => {
    try {
        const response = await fetch('/signout', {
            method: 'POST'
        });

        if (response.ok) {
            window.location.href = '/';
        }
    } catch (error) {
        showNotification('Error signing out', 'error');
    }
});

// Load today's birthdays
async function loadTodayBirthdays() {
    try {
        const response = await fetch('/api/birthdays/today');
        const birthdays = await response.json();

        const container = document.getElementById('today-birthdays');
        const emptyState = document.getElementById('no-today-birthdays');

        if (birthdays.length === 0) {
            container.innerHTML = '';
            emptyState.style.display = 'block';
        } else {
            emptyState.style.display = 'none';
            container.innerHTML = birthdays.map(bday => createBirthdayCard(bday, true)).join('');
        }
    } catch (error) {
        showNotification('Error loading today\'s birthdays', 'error');
    }
}

// Load upcoming birthdays
async function loadUpcomingBirthdays() {
    try {
        const response = await fetch('/api/birthdays');
        const birthdays = await response.json();

        const container = document.getElementById('upcoming-birthdays');
        const emptyState = document.getElementById('no-birthdays');

        if (birthdays.length === 0) {
            container.innerHTML = '';
            emptyState.style.display = 'block';
        } else {
            emptyState.style.display = 'none';
            container.innerHTML = birthdays.map(bday => createBirthdayCard(bday, false)).join('');
        }
    } catch (error) {
        showNotification('Error loading birthdays', 'error');
    }
}

// Create birthday card HTML
function createBirthdayCard(bday, isToday) {
    const imageHtml = bday.image
        ? `<img src="${bday.image}" alt="${bday.name}" class="birthday-image">`
        : `<div class="birthday-image-placeholder">🎂</div>`;

    const relationshipHtml = bday.relationship
        ? `<div class="birthday-relationship">${bday.relationship}</div>`
        : '';

    const date = new Date(bday.bdate);
    const formattedDate = date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });

    const countdownHtml = isToday
        ? `<div class="birthday-countdown">🎉 Today!</div>`
        : `<div class="birthday-countdown">In ${bday.days_until} day${bday.days_until !== 1 ? 's' : ''}</div>`;

    const ageHtml = bday.age
        ? `<div class="birthday-age">Turning ${bday.age}</div>`
        : '';

    return `
        <div class="birthday-card ${isToday ? 'today' : ''}" onclick="viewBirthday(${bday.id})">
            ${imageHtml}
            <div class="birthday-name">${bday.name}</div>
            ${relationshipHtml}
            <div class="birthday-date">${formattedDate}</div>
            ${countdownHtml}
            ${ageHtml}
        </div>
    `;
}

// View birthday details
async function viewBirthday(birthdayId) {
    try {
        const response = await fetch('/api/birthdays');
        const birthdays = await response.json();
        const birthday = birthdays.find(b => b.id === birthdayId);

        if (!birthday) {
            showNotification('Birthday not found', 'error');
            return;
        }

        currentBirthdayId = birthdayId;

        const imageHtml = birthday.image
            ? `<img src="${birthday.image}" alt="${birthday.name}" class="detail-image">`
            : `<div class="detail-image-placeholder">🎂</div>`;

        const date = new Date(birthday.bdate);
        const formattedDate = date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });

        const detailsHtml = `
            ${imageHtml}
            <div class="detail-item">
                <div class="detail-label">Name</div>
                <div class="detail-value">${birthday.name}</div>
            </div>
            ${birthday.relationship ? `
                <div class="detail-item">
                    <div class="detail-label">Relationship</div>
                    <div class="detail-value">${birthday.relationship}</div>
                </div>
            ` : ''}
            <div class="detail-item">
                <div class="detail-label">Birth Date</div>
                <div class="detail-value">${formattedDate}</div>
            </div>
            ${birthday.age ? `
                <div class="detail-item">
                    <div class="detail-label">Age</div>
                    <div class="detail-value">${birthday.age} years old</div>
                </div>
            ` : ''}
            ${birthday.days_until !== undefined ? `
                <div class="detail-item">
                    <div class="detail-label">Next Birthday</div>
                    <div class="detail-value">In ${birthday.days_until} day${birthday.days_until !== 1 ? 's' : ''}</div>
                </div>
            ` : ''}
            ${birthday.memo ? `
                <div class="detail-item">
                    <div class="detail-label">Memo</div>
                    <div class="detail-value detail-memo">${birthday.memo}</div>
                </div>
            ` : ''}
        `;

        document.getElementById('birthday-details').innerHTML = detailsHtml;
        document.getElementById('view-modal').classList.add('show');
    } catch (error) {
        showNotification('Error loading birthday details', 'error');
    }
}

// Close view modal
document.getElementById('close-view-modal').addEventListener('click', () => {
    document.getElementById('view-modal').classList.remove('show');
});

// Edit birthday from view modal
document.getElementById('edit-birthday-btn').addEventListener('click', async () => {
    document.getElementById('view-modal').classList.remove('show');

    try {
        const response = await fetch('/api/birthdays');
        const birthdays = await response.json();
        const birthday = birthdays.find(b => b.id === currentBirthdayId);

        if (!birthday) {
            showNotification('Birthday not found', 'error');
            return;
        }

        // Populate form
        document.getElementById('modal-title').textContent = 'Edit Birthday';
        document.getElementById('birthday-id').value = birthday.id;
        document.getElementById('name').value = birthday.name;
        document.getElementById('relationship').value = birthday.relationship || '';
        document.getElementById('bdate').value = birthday.bdate;
        document.getElementById('memo').value = birthday.memo || '';

        // Show existing image
        if (birthday.image) {
            document.getElementById('image-preview').innerHTML = `<img src="${birthday.image}" alt="Preview">`;
        }

        document.getElementById('submit-btn').textContent = 'Update Birthday';
        document.getElementById('birthday-modal').classList.add('show');
    } catch (error) {
        showNotification('Error loading birthday for editing', 'error');
    }
});

// Delete birthday
document.getElementById('delete-birthday-btn').addEventListener('click', async () => {
    if (!confirm('Are you sure you want to delete this birthday?')) {
        return;
    }

    try {
        const response = await fetch(`/api/birthdays/${currentBirthdayId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
            showNotification(data.message, 'success');
            document.getElementById('view-modal').classList.remove('show');
            loadTodayBirthdays();
            loadUpcomingBirthdays();
        } else {
            showNotification(data.error, 'error');
        }
    } catch (error) {
        showNotification('Error deleting birthday', 'error');
    }
});

// Add birthday button
document.getElementById('add-birthday-btn').addEventListener('click', () => {
    resetForm();
    document.getElementById('modal-title').textContent = 'Add Birthday';
    document.getElementById('submit-btn').textContent = 'Save Birthday';
    document.getElementById('birthday-modal').classList.add('show');
});

// Upload button
document.getElementById('upload-btn').addEventListener('click', () => {
    document.getElementById('image').click();
});

// Image selection
document.getElementById('image').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        showNotification('Image size must be less than 5MB', 'error');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        currentImageBase64 = e.target.result;
        document.getElementById('image-preview').innerHTML = `<img src="${e.target.result}" alt="Preview">`;
    };
    reader.readAsDataURL(file);
});

// Close modal
document.getElementById('close-modal').addEventListener('click', () => {
    document.getElementById('birthday-modal').classList.remove('show');
});

document.getElementById('cancel-btn').addEventListener('click', () => {
    document.getElementById('birthday-modal').classList.remove('show');
});

// Birthday form submit
document.getElementById('birthday-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const birthdayId = document.getElementById('birthday-id').value;
    const name = document.getElementById('name').value;
    const relationship = document.getElementById('relationship').value;
    const bdate = document.getElementById('bdate').value;
    const memo = document.getElementById('memo').value;

    const data = {
        name,
        relationship,
        bdate,
        memo
    };

    if (currentImageBase64) {
        data.image = currentImageBase64;
    }

    try {
        let response;
        if (birthdayId) {
            // Update existing birthday
            response = await fetch(`/api/birthdays/${birthdayId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
        } else {
            // Add new birthday
            response = await fetch('/api/birthdays', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
        }

        const result = await response.json();

        if (response.ok) {
            showNotification(result.message, 'success');
            document.getElementById('birthday-modal').classList.remove('show');
            resetForm();
            loadTodayBirthdays();
            loadUpcomingBirthdays();
        } else {
            showNotification(result.error, 'error');
        }
    } catch (error) {
        showNotification('Error saving birthday', 'error');
    }
});

// Reset form
function resetForm() {
    document.getElementById('birthday-form').reset();
    document.getElementById('birthday-id').value = '';
    document.getElementById('image-preview').innerHTML = '';
    currentImageBase64 = null;
    currentBirthdayId = null;
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Close modal on outside click
document.getElementById('birthday-modal').addEventListener('click', (e) => {
    if (e.target.id === 'birthday-modal') {
        document.getElementById('birthday-modal').classList.remove('show');
    }
});

document.getElementById('view-modal').addEventListener('click', (e) => {
    if (e.target.id === 'view-modal') {
        document.getElementById('view-modal').classList.remove('show');
    }
});
