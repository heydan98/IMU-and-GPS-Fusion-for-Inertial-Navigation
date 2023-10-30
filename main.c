#include "myshm.h"
#include <math.h>
#include "MadgwickAHRS.h"
#include <time.h>
#include "quaternion_rotate.h"

void quaternion_to_euler(float w, float x, float y, float z, float *X, float *Y, float *Z){
    float t0 = 2 * (w * x + y * z);
    float t1 = 1 - 2 * (x * x + y * y);
    *X = atan2(t0, t1);

    float t2 = 2 * (w * y - z * x);
    t2 = (t2 > 1) ? 1 : t2;
    t2 = (t2 < -1) ? -1 : t2;
    *Y = asin(t2);

    float t3 = 2 * (w * z + x * y);
    float t4 = 1 - 2 * (y * y + z * z);
    *Z = atan2(t3, t4);
}
int main()
{   
    float check_new[2];
    char zero[]= "0";
    clock_t tic = clock();
    clock_t toc = clock();

    float X, Y, Z;
    int count = 0;
    myshm a;
    myshm a_1;

    char c[25 * 12];
    char c_1[2];
    myshm_init(&a, 25 * 12, 112, 0644);
    myshm_init(&a_1, 4, 113, 0666);

    while (1)
    {
        toc = clock();

        if (((double)(toc - tic) / CLOCKS_PER_SEC) >= 0.01)
        {
            // printf(" time %f \n", (double)(toc - tic) / CLOCKS_PER_SEC);
            tic = clock();
            count ++;
            myshm_read(&a, c);  
            
            // printf(" data %s \n", c);
            float calibrated_data[11];
            int data = sscanf(c, "%f %f %f %f %f %f %f %f %f %f %f",
                               &calibrated_data[0], &calibrated_data[1], &calibrated_data[2], &calibrated_data[3],
                               &calibrated_data[4], &calibrated_data[5], &calibrated_data[6], &calibrated_data[7],
                               &calibrated_data[8], &calibrated_data[9], &calibrated_data[10]);
            

            // for (int i = 0; i < 9; i++)
            // {
            //     printf("%.15f\n", calibrated_data[i]);
            // }

            MadgwickAHRSupdate(calibrated_data[3] * M_PI / 180, calibrated_data[4] * M_PI / 180, calibrated_data[5] * M_PI / 180, calibrated_data[0], calibrated_data[1], calibrated_data[2], calibrated_data[6] * 0.01, calibrated_data[7] * 0.01, calibrated_data[8] * 0.01);
            // printf("\n Q: %f,%f,%f,%f", q0, q1, q2, q3);

            quaternion_to_euler(q0, q1, q2, q3, &X, &Y, &Z); 
            // printf("\n X,Y,Z:%f,%f,%f", X, Y, Z);
            // printf("\n euler: %f,%f,%f", X*180/M_PI, Y*180/M_PI, Z*180/M_PI);
            qv_mult(q0, q1, q2, q3, 0.0, 0.0, 9.8);
            // printf("\n Q_mult_output: %f,%f,%f, %f", q_mult_output[0], q_mult_output[1], q_mult_output[2], q_mult_output[3]);
            // if (count >=100){
            myshm_read(&a_1, c_1); 
            int check_new;
            sscanf(c_1, "%d", &check_new);
            printf("Check new %d\n",&check_new);
            if (check_new == 1){
                printf("------------------------------------------------\n");
                printf("check new %d\n", &check_new);
                printf("lat %f, lng %f\n", calibrated_data[9], calibrated_data[10]);
                myshm_write(&a_1, &zero);
            
                strcpy(c_1, zero);
                check_new = 0;
                // count = 0;
            }
            // }
        
        }
    }

    return 0;
}
