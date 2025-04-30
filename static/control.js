/**
 * showProgressBar()
 * Displays and animates the <progress> element during long-running actions.
 */

function showProgressBar() {
  const bar = document.getElementById('progress-bar');

  bar.style.display = 'block';
  bar.value = 0;

  let progress = 0;

  const interval = setInterval(() => {
    if (progress >= 100) {
      clearInterval(interval);
      bar.style.display = 'none';
    } else {
      progress += 10;
      bar.value = progress;
    }
  }, 50);
}

/**
 * exportCSV()
 * Triggers CSV download via the /export endpoint,
 * passing current filter values as query parameters.
 */

function exportCSV() {
  showProgressBar();

  const platform = encodeURIComponent(document.getElementById('platform').value);
  const contentType = encodeURIComponent(document.getElementById('content_type').value);
  const sortBy = encodeURIComponent(document.getElementById('sort_by').value);

  setTimeout(() => {
    window.location.href = `/export?platform=${platform}&content_type=${contentType}&sort_by=${sortBy}`;
  }, 500);
}