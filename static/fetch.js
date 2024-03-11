fetch('http://127.0.0.1:5000/mushrooms')
    .then(response => response.json())
    .then(data => {
        const mushrooms = data;
        const mushroom5 = mushrooms[4];

        console.log(mushroom5);
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
