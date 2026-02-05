document.addEventListener('DOMContentLoaded', () => {

  document.querySelectorAll('[data-delete-url]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();

      const url = btn.dataset.deleteUrl;
      const name = btn.dataset.deleteName || 'this item';
      const redirectUrl = btn.dataset.deleteRedirect || null;

      Swal.fire({
        title: 'Confirm delete',
        html: `Are you sure you want to delete <b>${name}</b>?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel'
      }).then(result => {
        if (result.isConfirmed) {
          deleteObject(url, redirectUrl);
        }
      });
    });
  });

  function deleteObject(url, redirectUrl) {
    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    }).then(res => {
      if (res.ok) {
        if (redirectUrl) {
          window.location.href = redirectUrl;
        } else {
          location.reload();
        }
      }
      else {
        // TODO ERROR TOAST
      }
    });
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
      document.cookie.split(';').forEach(cookie => {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        }
      });
    }
    return cookieValue;
  }

});