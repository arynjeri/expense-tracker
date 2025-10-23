let incomeChart = null;
let expenseChart = null;

function currencyFmt(n) {
  return Number(n).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

async function initDashboard() {
  const res = await fetch('/api/transactions');
  const data = await res.json();

  document.getElementById('total-income').innerText = "KSh " + currencyFmt(data.summary.total_income || 0);
  document.getElementById('total-expense').innerText = "KSh " + currencyFmt(data.summary.total_expense || 0);
  document.getElementById('balance').innerText = "KSh " + currencyFmt(data.summary.balance || 0);

  const tbody = document.getElementById('transactions-tbody');
  tbody.innerHTML = '';
  data.transactions.slice().reverse().forEach(tr => {
    const trEl = document.createElement('tr');
    trEl.innerHTML = `
      <td class="p-2 border-b">${tr.id}</td>
      <td class="p-2 border-b capitalize">${tr.type}</td>
      <td class="p-2 border-b">${currencyFmt(tr.amount)}</td>
      <td class="p-2 border-b">${tr.description || ''}</td>
      <td class="p-2 border-b">${tr.date}</td>
    `;
    tbody.appendChild(trEl);
  });

  const dates = data.timeseries.dates || [];
  const incomeSeries = data.timeseries.income || [];
  const expenseSeries = data.timeseries.expense || [];

  const incomeCtx = document.getElementById('incomeChart').getContext('2d');
  const expenseCtx = document.getElementById('expenseChart').getContext('2d');

  if (incomeChart) incomeChart.destroy();
  if (expenseChart) expenseChart.destroy();

  incomeChart = new Chart(incomeCtx, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [{
        label: 'Income',
        data: incomeSeries,
        borderColor: 'rgb(34,197,94)',
        backgroundColor: 'rgba(34,197,94,0.1)',
        tension: 0.3
      }]
    },
    options: {
      scales: { y: { beginAtZero: true } },
      plugins: { legend: { display: false } }
    }
  });

  expenseChart = new Chart(expenseCtx, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [{
        label: 'Expense',
        data: expenseSeries,
        borderColor: 'rgb(239,68,68)',
        backgroundColor: 'rgba(239,68,68,0.1)',
        tension: 0.3
      }]
    },
    options: {
      scales: { y: { beginAtZero: true } },
      plugins: { legend: { display: false } }
    }
  });
}
