

// Master Object


let DIM = 3;
let maxiterations = 3;
let targetDIM = 180; 
let targetMaxIterations = 10; 
let transitionSpeed = 1; 
let mandelbulb = [];
let transitioning = true;

function setup() {
  const canvas = createCanvas(800, 800, WEBGL);
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
        let n = 2.428775629752634; 
        let iteration = 3;
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
          mandelbulb.push(createVector(x * 200, y * 200, z * 200)); // Scale for visibility
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
  strokeWeight(0.1);
  stroke(255);
  noFill();
  rotateX(HALF_PI); // Rotate to make the Mandelbulb stand upright
  rotateZ(frameCount * 0.02); // Add rotation around the Y-axis
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
  if (abs(DIM - targetDIM) > 0.1) {
    DIM = lerp(DIM, targetDIM, transitionSpeed);
    needRecalculation = true;
  }
  if (abs(maxiterations - targetMaxIterations) > 0.1) {
    maxiterations = lerp(maxiterations, targetMaxIterations, transitionSpeed);
    needRecalculation = true;
  }
  
  if (needRecalculation) {
    calculateMandelbulb(floor(DIM), floor(maxiterations));
  } else {
    transitioning = true; 
  }
}

//transitionToNewValues(100, 50);
