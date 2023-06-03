#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <time.h>
#include <string.h>
#include "MQTTClient.h"

#define I2C_SLAVE       0x0703
#define I2C_SENSOR_ADDR 0x40
#define SENSOR_TEMP     0xF3
#define SENSOR_HUMID    0xF5

#define QOS         1
#define TIMEOUT     10000L

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

void set_payload(char* payload_buf, char* argv[], int fd) 
{
    char* payload_template = 
        "{\"device_id\": %d, \"time\": %s,"
        "\"data\": {\"temp_c\": %f, \"hum\": %f}}";

    int device_id = atoi(argv[3]);
    if (device_id == 0) 
    {
        printf("Error: Invalid device_id\n");
        exit(EXIT_FAILURE);
    }

    time_t raw_time = time(NULL);
    struct tm* datetime_utc = gmtime(&raw_time);
    char time_buf[50];
    strftime(time_buf, 50, "%F %T UTC\n", datetime_utc);

    sprintf(payload_buf, payload_template, device_id, 
        time_buf, get_temperatue(fd), get_humidity(fd));
}

// Arguments list: <broker_address> <topic> <device_id>
// Example: ./client 111.222.33.44:1883 topic1 1
int main(int argc, char* argv[])
{
    if (argc < 4)
    {
        printf("Error: Invalid amount of arguments (should be 4)\n");
        exit(3);
    }
    
    const char* device = "/dev/i2c-1";
    int fd;

    if ((fd = open(device, O_RDWR)) < 0)
        exit(1);

    if (ioctl(fd, I2C_SLAVE, I2C_SENSOR_ADDR) < 0)
        exit(2);

    char* address = argv[1];
    char* topic   = argv[2];
    
    char* client_id;
    asprintf(&client_id, "client_%s", argv[3]);

    MQTTClient client;
    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
    MQTTClient_message pubmsg = MQTTClient_message_initializer;
    MQTTClient_deliveryToken token;
    int rc;
 
    if ((rc = MQTTClient_create(&client, address, client_id,
        MQTTCLIENT_PERSISTENCE_NONE, NULL)) != MQTTCLIENT_SUCCESS)
    {
        printf("Failed to create client, return code %d\n", rc);
        exit(EXIT_FAILURE);
    }
 
    conn_opts.keepAliveInterval = 20;
    conn_opts.cleansession = 1;
    if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS) 
    {
        printf("Failed to connect, return code %d\n", rc);
        exit(EXIT_FAILURE);
    }
    
    char payload_buf[1000];
    set_payload(payload_buf, argv, fd);

    pubmsg.payload = payload_buf;
    pubmsg.payloadlen = (int)strlen(pubmsg.payload);
    pubmsg.qos = QOS;
    pubmsg.retained = 0;
    if ((rc = MQTTClient_publishMessage(client, topic, &pubmsg, &token)) != MQTTCLIENT_SUCCESS) 
    {
        printf("Failed to publish message, return code %d\n", rc);
        exit(EXIT_FAILURE);
    }
 
    rc = MQTTClient_waitForCompletion(client, token, TIMEOUT);
    printf("Message %s on topic %s was delivered\n", payload_buf, topic, token);
 
    if ((rc = MQTTClient_disconnect(client, 10000)) != MQTTCLIENT_SUCCESS)
        printf("Failed to disconnect, return code %d\n", rc);
    MQTTClient_destroy(&client);
    return rc;
}
