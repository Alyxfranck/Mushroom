let age;
let DIM;
let mandelbulb = [];
let size;

// Function to fetch data and update variables
function fetchData() {
  fetch('/mushroom')
    .then(response => response.json())
    .then(data => {
      size = 2.4 * 1/ data.size;
      age = 256 * 1/ data.age;
      DIM = age;
      setup();
    })
    .catch(error => console.error(error));
  console.log(DIM);
}

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  colorMode(RGB, 255);
  orbitControl(); // Enables mouse drag rotation

  for (let i = 0; i < DIM; i++) {
    for (let j = 0; j < DIM; j++) {
      for (let k = 0; k < DIM; k++) {
        let x = map(i, 0, DIM, -1, 1);
        let y = map(j, 0, DIM, -1, 1);
        let z = map(k, 0, DIM, -1, 1);
        let zeta = createVector(0, 0, 0);
        let n = size; // Adjusted for visual clarity
        let maxiterations = 23; // Adjusted for performance and clarity
        let iteration = 0;
        while (true) {
          let c = spherical(zeta.x, zeta.y, zeta.z);
          let newx = pow(c.r, n) * sin(c.theta * n) * cos(c.phi * n);
          let newy = pow(c.r, n) * sin(c.theta * n) * sin(c.phi * n);
          let newz = pow(c.r, n) * cos(c.theta * n);
          zeta.x = newx + x;
          zeta.y = newy + y;
          zeta.z = newz + z;
          iteration++;
          if (c.r > 2 || iteration > maxiterations) {
            break;
          }
        }
        if (iteration === maxiterations) {
          mandelbulb.push(createVector(x * 100, y * 100, z * 100)); // Scale for visibility
        }
      }
    }
  }
}

function spherical(x, y, z) {
  let r = sqrt(x * x + y * y + z * z);
  let theta = atan2(sqrt(x * x + y * y), z);
  let phi = atan2(y, x);
  return { r, theta, phi };
}

function draw() {
  background(0);

  strokeWeight(1); 
  stroke(255); // Set stroke to white for visibility
  noFill();

  
  beginShape(POINTS);
  for (let v of mandelbulb) {

    vertex(v.x, v.y, v.z);
  }
  endShape();
}
