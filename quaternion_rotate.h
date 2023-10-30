#ifndef quaternion_rotate_h
#define quaternion_rotate_h

double q_mult_output[4];
void q_mult(double w1, double x1, double y1, double z1, double w2, double x2, double y2, double z2)
{
    q_mult_output[0] = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2;
    q_mult_output[1] = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2;
    q_mult_output[2] = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2;
    q_mult_output[3] = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2;
}

void qv_mult(double q1_w, double q1_x, double q1_y, double q1_z, double v1_x, double v1_y, double v1_z)
{
    double v1_w = 0.0;
    q_mult(q1_w, q1_x, q1_y, q1_z, v1_w, v1_x, v1_y, v1_z);
    q_mult(q_mult_output[0], q_mult_output[1], q_mult_output[2], q_mult_output[3], q1_w, -q1_x, -q1_y, -q1_z);
    // output q_mult_output[1], q_mult_output[2], q_mult_output[3]. Coresponding to x,y,z
}

// Usage. Note: not thread safe
// void main(){
//     qv_mult(0.6532814824381883, 0.27059805007309845, 0.6532814824381882, 0.2705980500730985, 1, 0, 0);
//     printf("%f %f %f", q_mult_output[1], q_mult_output[2], q_mult_output[3]);
// }

#endif