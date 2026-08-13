const form = document.querySelector('#leave-form');
const listEl = document.querySelector('#leave-list');
const statusBar = document.querySelector('#status-bar');
const formError = document.querySelector('#form-error');

async function loadLeaves() {
  const response = await fetch('/api/leave-records?role=administrator');
  const data = await response.json();
  if (!response.ok) {
    statusBar.textContent = data.error?.message || 'Unable to load leave records';
    return;
  }

  const records = data.leave_requests || [];
  statusBar.textContent = records.length ? `Showing ${records.length} leave request(s)` : 'No leave requests yet';
  listEl.innerHTML = records.length
    ? records.map((item) => `
        <article class="leave-item">
          <div class="leave-item-header">
            <strong>${item.employee_id}</strong>
            <span class="status-chip status-${item.status}">${item.status}</span>
          </div>
          <div><strong>Manager:</strong> ${item.manager_id}</div>
          <div><strong>Type:</strong> ${item.leave_type}</div>
          <div><strong>Dates:</strong> ${item.start_date} → ${item.end_date}</div>
          <div><strong>Reason:</strong> ${item.reason}</div>
        </article>
      `).join('')
    : '<p>No leave requests available.</p>';
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  formError.hidden = true;
  formError.className = 'alert error';

  const payload = {
    employee_id: document.querySelector('#employee_id').value.trim(),
    manager_id: document.querySelector('#manager_id').value.trim(),
    leave_type: document.querySelector('#leave_type').value,
    start_date: document.querySelector('#start_date').value,
    end_date: document.querySelector('#end_date').value,
    reason: document.querySelector('#reason').value.trim(),
  };

  try {
    const response = await fetch('/api/leave-requests', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) {
      const fields = data.error?.fields || {};
      const messages = Object.entries(fields).map(([key, value]) => `${key}: ${value}`);
      formError.textContent = messages.join(' | ') || data.error?.message || 'Could not create leave request';
      formError.hidden = false;
      return;
    }

    formError.textContent = 'Leave request created successfully.';
    formError.className = 'alert success';
    formError.hidden = false;
    form.reset();
    await loadLeaves();
  } catch (error) {
    formError.textContent = 'The leave API is unavailable.';
    formError.hidden = false;
  }
});

loadLeaves();
