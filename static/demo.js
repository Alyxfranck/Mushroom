
fetch('http://127.0.0.1:5000/mushrooms')
    .then(response => response.json())
    .then(data => {
            // Assuming data is an array and you want the first item
            const Mushroom1 = data[0];
            size = 2.5 * 2 / Mushroom1.size;
            age = 256 * 1 / Mushroom1.age;
            DIM = age; // Not sure what DIM is for, but assigning age to it
            console.log(size);
            console.log(age);
            console.log(DIM); // Log the size of the first mushroom
        });