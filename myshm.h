#ifndef MYSHM_H // OBJECT
#define MYSHM_H

#include<stdio.h>
#include<sys/ipc.h>
#include<sys/shm.h>
#include<sys/types.h>
#include<string.h>
#include<errno.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>

typedef struct {
    int size, key, flag;  /*size is the size of share mem by byte, key is the address, flag is configuration of permission and stuff*/
    void *shmp;
} myshm;  /*Object*/

int myshm_init(myshm * const self, int size, int key , int flag);
int myshm_write(myshm * const self, void  * data_write);
int myshm_read(myshm * const self, void * data_read);

#endif