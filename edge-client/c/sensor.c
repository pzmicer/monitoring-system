#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <time.h>

#define I2C_SLAVE       0x0703
#define I2C_SENSOR_ADDR 0x40
#define SENSOR_TEMP     0xF3
#define SENSOR_HUMID    0xF5


void delay(unsigned int millisec)
{
    struct timespec sleeper, empty;
    sleeper.tv_sec  = (time_t)(millisec / 1000);
    sleeper.tv_nsec = (long)(millisec % 1000) * 1000000;
    nanosleep(&sleeper, &empty);
}

double get_temperatue(int fd)
{
    unsigned char buf[4];
    unsigned char command = SENSOR_TEMP;

    write(fd, &command, 1);
    delay(100);
    read(fd, buf, 3);

    unsigned int s_temp = (buf[0] << 8 | buf[1]) & 0xFFFC;
    double temp = s_temp / 65536.0;
    return -46.85 + (175.72 * temp);
}

double get_humidity(int fd)
{
    unsigned char buf[4];
    unsigned char command = SENSOR_HUMID;

    write(fd, &command, 1);
    delay(100);
    read(fd, buf, 3);

    unsigned int s_rh = (buf[0] << 8 | buf[1]) & 0xFFFC;
    double rh = s_rh / 65536.0;
    return -6.0 + (125.0 * rh);
}

int main()
{
    const char* device = "/dev/i2c-1";
    int fd;

    if ((fd = open(device, O_RDWR)) < 0)
        exit(1);

    if (ioctl(fd, I2C_SLAVE, I2C_SENSOR_ADDR) < 0)
        exit(2);

    double temp = get_temperatue(fd);
    double hum  = get_humidity(fd);

    printf("Temperature = %5.2fC\nHumidity = %5.2f%%RH\n", temp, hum);
    return 0;
}
