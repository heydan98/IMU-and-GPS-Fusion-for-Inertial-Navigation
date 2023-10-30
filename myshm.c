#include "myshm.h"

int myshm_init(myshm *const self, int size, int key, int flag)
{

    self->size = size;
    self->key = key;
    self->flag = flag;
    
    int shmid;
   
    shmid = shmget(self->key, self->size, self->flag); // get access to page address, 0644 is authorization, key's also the address
    if (shmid == -1)
    { // check if success
        perror("Shared memory");
        return 1;
    }
    // Attach to the segment to get a pointer to it.
    self->shmp  = shmat(shmid, NULL, 0); // bind virtual memory to shmp which is a instance of shmseg
    if (self->shmp  == (void *)-1)
    { // check if success
        perror("Shared memory attach");
    }

    return 0;

}

int myshm_write(myshm *const self, void * data_write)
{   
    memcpy(self->shmp, data_write, self->size );    
    return 0;
}

int myshm_read(myshm *const self, void * data_read)
{   
    
    memcpy(data_read, self->shmp, self->size  );
    
    return 0;
}

