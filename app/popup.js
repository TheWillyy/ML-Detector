document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#detectButton').addEventListener('click', () => {
        document.getElementById("result").innerHTML = ``
        const urlTemp = document.querySelector('#detectInput').value;
        const url = !/^https?:\/\//i.test(urlTemp) ? `http://${urlTemp}` : urlTemp;

        fetch('http://0.0.0.0:5001/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "url" : `${url}`
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            document.getElementById("result").innerHTML = `${data.is_malicious? "This URL is Malicious" : "The URL is safe"}`
            // Process and display data
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    });
});