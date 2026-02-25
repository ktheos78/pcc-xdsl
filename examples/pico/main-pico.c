#include "pico/stdlib.h"

extern int compiled_asm(void);

int main(void)
{
    int res, delay;

    stdio_init_all();

    const uint LED_PIN = PICO_DEFAULT_LED_PIN;
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    // tune delay according to assembly return value
    res = compiled_asm();
    delay = (res * 1000 < 50) ? 50 : (res * 3);

    // main loop
    while (1)
    {
        gpio_put(LED_PIN, 1);
        sleep_ms(delay);
        gpio_put(LED_PIN, 0);
        sleep_ms(delay);
    }
}