#include <stdio.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#define KEY 1025
#define SIZE 5
int main(int argc, char **argv)
{
    
    int shmid;
    shmid = shmget(KEY, SIZE, 0644 ); // get access to page address, size = shmseg, 0644 is authorization, key = SHM_KEY it's also the address
    if (shmid == -1)
    {
        perror("Shared memory");
        return 1;
    }
   
    shmctl(shmid1, IPC_RMID, NULL);
}