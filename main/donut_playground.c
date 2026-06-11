#include <stdio.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_chip_info.h"
#include "esp_idf_version.h"

void app_main(void)
{
    esp_chip_info_t chip;
    esp_chip_info(&chip);

    printf("donut-playground ready\n");
    printf("target: %s, cores: %d, idf: %s\n", CONFIG_IDF_TARGET, chip.cores,
           esp_get_idf_version());

    int n = 0;
    while (true) {
        printf("tick %d\n", n++);
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}
