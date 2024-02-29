The code provided runs two motors to a desired setpoint simultaneously using multitasking, setting each motor task to a period of 20 ms. In order to find this value, we conducted response testing. We increased the period of one motor task from 1 ms, then to 5 ms, then continued increasing in increments of 5 ms until we noticed our response worsened signifigantly. Below, we can see the results of our testing
![5 ms- very nice](https://github.com/squidulvick/Lab4/assets/156977553/971bd557-8b7c-4ea0-b41f-92b947888648)
from the plot above we can see a nice clean response that results from a short period. However, 5 ms is a bit overkil.
![25-ms - nominal nice](https://github.com/squidulvick/Lab4/assets/156977553/dad1579a-44c9-4580-91a8-c902637d2c60)
The above plot is the smallest period value where the response is significantly changed. Increasing it furthur results in the following plot (with a 50 ms period) showing the extreme.
![50 ms plot-no good](https://github.com/squidulvick/Lab4/assets/156977553/84ef96bb-5bee-46dd-9c87-7f259ae4ac47)
TSo, from our testing, we want a value around 20 ms to give us some cushion. This balances the overkill and worsened results. The 20 ms response can be seen below.
![20 ms- da best](https://github.com/squidulvick/Lab4/assets/156977553/db2be60b-c56a-4a52-97c5-0c380f929279)

