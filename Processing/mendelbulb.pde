import peasy.*;

int DIM = 100;
PeasyCam cam;
ArrayList<PVector> mandelbulb = new ArrayList<PVector>();

void setup() {
  size(1000, 1000, P3D);
  cam = new PeasyCam(this, 1000);
  colorMode(RGB, 255);  StringList points = new StringList();

  for (int i = 0; i < DIM; i++) {
    for (int j = 0; j < DIM; j++) {
      boolean edge = false;
      for (int k = 0; k < DIM; k++) {
        float x = map(i, 0, DIM, -1, 1);
        float y = map(j, 0, DIM, -1, 1);
        float z = map(k, 0, DIM, -1, 1);
        PVector zeta = new PVector(0, 0, 0);
        float n = 2.32243432424;
        int maxiterations = 200;
        int iteration = 0;
        while (true) {
          Spherical c = spherical(zeta.x, zeta.y, zeta.z);
          float newx = pow(c.r, n) * sin(c.theta*n) * cos(c.phi*n);
          float newy = pow(c.r, n) * sin(c.theta*n) * sin(c.phi*n);
          float newz = pow(c.r, n) * cos(c.theta*n);
          zeta.x = newx + x;
          zeta.y = newy + y;
          zeta.z = newz + z;
          iteration++;
          if (c.r > 16) {
            if (edge) {
              edge = false;
            }
            break;
          }
          if (iteration > maxiterations) {
            if (!edge) {
              edge = true;
              mandelbulb.add(new PVector(x, y, z));
            }
            break;
          }
        }
      }
    }
  }
  
  String[] output = new String[mandelbulb.size()];
  for (int i = 0; i < output.length; i++) {
    PVector v = mandelbulb.get(i);
    output[i] = v.x + " " + v.y + " " + v.z;
  }
  saveStrings("mandelbulb.txt", output);
  
}

class Spherical {
  float r, theta, phi;
  Spherical(float r, float theta, float phi) {
    this.r = r;
    this.theta = theta;
    this.phi = phi;
  }
}

Spherical spherical(float x, float y, float z) {
  float r = sqrt(x*x + y*y + z*z);
  float theta = atan2( sqrt(x*x+y*y), z);
  float phi = atan2(y, x);
  return new Spherical(r, theta, phi);
}
void drawAxes(float length) {
  strokeWeight(2); // Set the stroke weight to make the axes more visible
  
  // X-axis in red
  stroke(255, 0, 0);
  line(0, 0, 0, length, 0, 0);
  
  // Y-axis in green
  stroke(0, 255, 0);
  line(0, 0, 0, 0, length, 0);
  
  // Z-axis in blue
  stroke(0, 0, 255);
  line(0, 0, 0, 0, 0, length);
  
  // Resetting stroke weight
  strokeWeight(1);
}
void draw() {
  background(0);
  rotateX(-200);  
  drawAxes(500);


  for (PVector v : mandelbulb) {
    float red = map(v.x, -1, 1, 0, 255);
    float green = map(v.y, -1, 1, 0, 255);
    float blue = map(v.z, -1, 1, 0, 255);

    stroke(red, green, blue);
    strokeWeight(1); // Adjust point size as needed
    point(v.x * 200, v.y * 200, v.z * 200);
  }
}
