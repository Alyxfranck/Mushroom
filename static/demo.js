fetch('/mushroom')
  .then(response => response.json())
  .then(data => {
    size = data.size;
    age = data.age;
    DIM = age;
    setup();
  })
  .catch(error => console.error(error));
  console.log(DIM);
  