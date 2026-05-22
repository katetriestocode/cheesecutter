function submit() {
    const linkvalue = document.getElementById('link').value;
    const summarytext = document.getElementById('summarytext');

    if (!linkvalue) {
        alert('paint a link first :P');
        return;
    }

    summarytext.innerText = 'cheesecutting...';

    fetch('/process', {
        method: 'post',
        headers: {
            'content-type': 'application/json',
        },
        body: JSON.stringify({link: linkvalue}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.summary) {
            summarytext.innerText = data.summary;
        } else {
            summarytext.innerText = "oopsy daisy";
        }
    })
    .catch(error => {
        console.error('error:', error);
        summarytext.innerText = "oopsy doopsy";
    });
}