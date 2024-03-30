document.getElementById('worker-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch('/add_worker', {
        method: 'POST',
        body: formData
    });
    alert(await response.text());
    });
    
document.getElementById('patron-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch('/add_patron', {
        method: 'POST',
        body: formData
    });
    alert(await response.text());
    });