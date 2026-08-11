const form = document.querySelector('#claim-form');
const formPanel = document.querySelector('[data-step="1"]');
const reviewPanel = document.querySelector('[data-step="2"]');
const formError = document.querySelector('#form-error');
const submitError = document.querySelector('#submit-error');
const losses = document.querySelector('#losses');
const documents = document.querySelector('#documents');
let currentClaimId = null;

const escapeHtml = (value) => String(value ?? '').replace(/[&<>'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#039;', '"': '&quot;' })[character]);
const field = (id) => document.querySelector(`#${id}`).value.trim();

function addLoss(data = {}) {
  const row = document.createElement('div');
  row.className = 'repeat-row';
  row.innerHTML = `<input aria-label="Expense description" data-loss="description" placeholder="Description" value="${escapeHtml(data.description)}"><input aria-label="Expense amount" data-loss="amount" type="number" min="0" step="0.01" placeholder="Amount" value="${escapeHtml(data.amount)}"><input aria-label="Expense currency" data-loss="currency" maxlength="3" placeholder="USD" value="${escapeHtml(data.currency || 'USD')}"><button type="button" class="remove" aria-label="Remove expense">×</button>`;
  row.querySelector('.remove').addEventListener('click', () => row.remove());
  losses.appendChild(row);
}

function addDocument(data = {}) {
  const row = document.createElement('div');
  row.className = 'repeat-row document-row';
  row.innerHTML = `<input aria-label="Document name" data-document="name" placeholder="Document or receipt name" value="${escapeHtml(data.name)}"><select aria-label="Document status" data-document="status"><option>Provided</option><option>Missing</option><option>Not applicable</option></select><button type="button" class="remove" aria-label="Remove document">×</button>`;
  row.querySelector('select').value = data.status || 'Provided';
  row.querySelector('.remove').addEventListener('click', () => row.remove());
  documents.appendChild(row);
}

function collectClaim() {
  const claim = {
    insurance_type: field('insurance_type'), insurer: field('insurer'), policy_number: field('policy_number'), claim_reference: field('claim_reference'), incident_date: field('incident_date'), location: field('location'), description: field('description'),
    losses: [...losses.children].map((row) => ({ description: row.querySelector('[data-loss="description"]').value.trim(), amount: Number(row.querySelector('[data-loss="amount"]').value || 0), currency: row.querySelector('[data-loss="currency"]').value.trim().toUpperCase() })).filter((item) => item.description),
    documents: [...documents.children].map((row) => ({ name: row.querySelector('[data-document="name"]').value.trim(), status: row.querySelector('[data-document="status"]').value })).filter((item) => item.name),
  };
  return claim;
}

function showFieldErrors(fields = {}) {
  document.querySelectorAll('.field-error').forEach((input) => input.classList.remove('field-error'));
  const labels = { insurance_type: 'Insurance type', insurer: 'Insurer', policy_number: 'Policy number', incident_date: 'Incident date', description: 'Description' };
  const messages = Object.entries(fields).map(([name, message]) => { document.querySelector(`#${name}`)?.classList.add('field-error'); return `${labels[name] || name}: ${message}`; });
  formError.textContent = messages.join(' | ') || 'Please check the highlighted fields.';
  formError.hidden = false;
}

function renderReview(claim) {
  const lossesMarkup = (claim.losses || []).length ? `<ul class="review-list">${claim.losses.map((item) => `<li>${escapeHtml(item.description)} · ${escapeHtml(item.currency)} ${escapeHtml(item.amount)}</li>`).join('')}</ul>` : '<p>None added</p>';
  const documentsMarkup = (claim.documents || []).length ? `<ul class="review-list">${claim.documents.map((item) => `<li>${escapeHtml(item.name)} · ${escapeHtml(item.status)}</li>`).join('')}</ul>` : '<p>None added</p>';
  document.querySelector('#review-content').innerHTML = `<div class="review-grid"><div class="review-block"><h3>Policy</h3><p><strong>${escapeHtml(claim.insurer)}</strong></p><p>${escapeHtml(claim.insurance_type)} · ${escapeHtml(claim.policy_number)}</p><p>${escapeHtml(claim.claim_reference || 'No claim reference')}</p></div><div class="review-block"><h3>Incident</h3><p><strong>${escapeHtml(claim.incident_date)}</strong> · ${escapeHtml(claim.location || 'Location not provided')}</p><p>${escapeHtml(claim.description)}</p></div><div class="review-block"><h3>Losses & expenses</h3>${lossesMarkup}</div><div class="review-block"><h3>Evidence</h3>${documentsMarkup}</div></div>`;
}

async function loadTypes() {
  try {
    const response = await fetch('/api/insurance-types');
    const data = await response.json();
    document.querySelector('#insurance_type').insertAdjacentHTML('beforeend', data.insurance_types.map((type) => `<option value="${escapeHtml(type)}">${escapeHtml(type[0].toUpperCase() + type.slice(1))}</option>`).join(''));
  } catch (error) { formError.textContent = 'The API is unavailable. Start the claims server and refresh this page.'; formError.hidden = false; }
}

async function createClaim(claim) {
  const response = await fetch('/api/claims', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(claim) });
  const data = await response.json();
  if (!response.ok) { showFieldErrors(data.error?.fields); throw new Error(data.error?.message || 'Could not save claim'); }
  return data.claim;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  formError.hidden = true;
  if (!form.checkValidity()) { form.reportValidity(); return; }
  try {
    const claim = await createClaim(collectClaim());
    currentClaimId = claim.id;
    renderReview(claim);
    formPanel.hidden = true; reviewPanel.hidden = false;
    document.querySelector('[data-step-indicator="1"]').classList.remove('active');
    document.querySelector('[data-step-indicator="2"]').classList.add('active');
  } catch (error) { if (formError.hidden) { formError.textContent = error.message; formError.hidden = false; } }
});

document.querySelector('#back-button').addEventListener('click', () => { reviewPanel.hidden = true; formPanel.hidden = false; });
document.querySelector('#add-loss').addEventListener('click', () => addLoss());
document.querySelector('#add-document').addEventListener('click', () => addDocument());
document.querySelector('#submit-button').addEventListener('click', async () => {
  submitError.hidden = true;
  try {
    const response = await fetch(`/api/claims/${currentClaimId}/submit`, { method: 'POST' });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error?.message || 'Could not submit claim');
    document.querySelector('.review-status').textContent = 'Submitted';
    document.querySelector('.review-status').style.background = '#d9eee3';
    document.querySelector('.review-status').style.color = '#27634d';
    document.querySelector('#submit-button').disabled = true;
    document.querySelector('#submit-button').textContent = 'Claim submitted';
  } catch (error) { submitError.textContent = error.message; submitError.hidden = false; }
});

addLoss();
addDocument();
loadTypes();
