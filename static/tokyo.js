
let DIM = 3;
let maxiterations = 2;
let targetDIM = 256; // Set the target dimension you want to transition to
let targetMaxIterations = 25; // Set the target max iterations you want to transition to
let transitionSpeed = 0.0000001; // Speed of the transition
let mandelbulb = [];
let transitioning = true;

function setup() {
  const canvas = createCanvas(800, 600, WEBGL);
  canvas.style('display', 'block');
  canvas.position((windowWidth - width) / 2, (windowHeight - height) / 2);
 
  calculateMandelbulb(DIM, maxiterations); // Initial calculation
}

function calculateMandelbulb(DIM, maxiterations) {
  mandelbulb = []; // Reset the array
  for (let i = 0; i < DIM; i++) {
    for (let j = 0; j < DIM; j++) {
      for (let k = 0; k < DIM; k++) {
        let x = map(i, 0, DIM, -2, 2);
        let y = map(j, 0, DIM, -2, 2);
        let z = map(k, 0, DIM, -2, 2);
        let zeta = createVector(0, 0, 0);
        let n = 2.4 ; // This is a parameter that determines the "power" of the Mandelbulb
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
   fetch('http://127.0.0.1:5000/mushrooms') 
    .then(response => response.json())
    .then(data => {
      // Extract the color value from the JSON data
      let color = data[0].color;

      // Set the stroke color based on the fetched color value
      stroke(color);
      strokeWeight(0.2);
    
      beginShape(POINTS);
      for (let v of mandelbulb) {
        vertex(v.x, v.y, v.z);
      }
      endShape();
    })
    .catch(error => {
      console.error('Error fetching JSON:', error);
    });

 

  rotateX(HALF_PI); // Rotate to make the Mandelbulb stand upright
  rotateZ(frameCount * 0.002); // Add rotation around the Y-axis

  // Render the Mandelbulb points
  beginShape(POINTS);
  for (let v of mandelbulb) {
    vertex(v.x, v.y, v.z);
  }
  endShape();

  if (transitioning) {
    updateValues();
  }
}

function transitionToNewValues(newDIM, newMaxIterations) {
  targetDIM = newDIM;
  targetMaxIterations = newMaxIterations;
  transitioning = true;
}

function updateValues() {
  let needRecalculation = false;
  // Use lerp to create a smooth transition for DIM
  if (abs(DIM - targetDIM) > 0.1) {
    DIM = lerp(DIM, targetDIM, transitionSpeed);
    needRecalculation = true;
  }
  // Use lerp to create a smooth transition for maxiterations
  if (abs(maxiterations - targetMaxIterations) > 0.1) {
    maxiterations = lerp(maxiterations, targetMaxIterations, transitionSpeed);
    needRecalculation = true;
  }
  
  // Recalculate the Mandelbulb if needed
  if (needRecalculation) {
    calculateMandelbulb(floor(DIM), floor(maxiterations));
  } else {
    transitioning = true; // Stop transitioning once the target values are reached
  }
}

// To initiate the transition, call the following function with your desired values:
// transitionToNewValues(100, 50);
