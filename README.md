The code provided runs two motors to a desired setpoint simultaneously using multitasking, setting each motor task to a period of 20 ms. TO find this value, we conducted response testing. We increased the period of one motor task from 1 ms, then to 5 ms, then continued increasing it until we noticed our response overshoot signifigantly. Below, we can see the results of our testing
![5 ms- very nice](https://github.com/squidulvick/Lab4/assets/156977553/971bd557-8b7c-4ea0-b41f-92b947888648)
from the plot above we can see a nice clean response that results from a short period. 
![25-ms - nominal nice](https://github.com/squidulvick/Lab4/assets/156977553/dad1579a-44c9-4580-91a8-c902637d2c60)
The above is plot is the smallest period value where the response is signigantly changed. Increasing it furthur results in the following plot. 
![50 ms plot-no good](https://github.com/squidulvick/Lab4/assets/156977553/84ef96bb-5bee-46dd-9c87-7f259ae4ac47)
So, from our testing, we want a value around 20 ms to give us some cushion. The 20 ms response can be seen below.
![20 ms- da best](https://github.com/squidulvick/Lab4/assets/156977553/db2be60b-c56a-4a52-97c5-0c380f929279)

