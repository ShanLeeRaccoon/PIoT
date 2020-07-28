from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
y = (255, 255, 0) #Yellow
b = (0, 0, 0) # Black
lg = (12,147,46) #light green
g = (19,133,52) # green
dg = (44, 123, 74) #dark green
dp = (188, 52, 198) # dark purple
p = (191, 74, 102) #purple
lp = (216, 171, 210) #light purple

r = (255, 0, 0) #red
bl = (74, 74, 255)#blue
w = (255, 255, 255) #white
gr = (50, 50, 50)#gray


eggplant_not_face = [
   b, b, b, b, b, lg, b, b,
   b, b, b, b, g, lg ,g, b,
   b, b, b, b, dg, g, dg, lg,
   b , b, lp, p, dp, dp, dp, b,
   b, lp, lp, p, dp, dp, lp, b,
   b , dp, dp, dp, dp, p, lp, b,
   b, dp, p, p, p, lp, lp, b,
   b, b, b, b, b, b, b, b,
]

angry_face = [
   y, r, r, r, r, r, r, y,
   r, y, r, r, r, r, y, r,
   r, b, y, r, r, y, b, r,
   r, b, b, y, y, b, b, r,
   r, y, y, y, y, y, y, r,
   y, w, r, w, r, w, r, y,
   y, r, w, r, w, r, w, y,
   r, y, y, y, y, y, y, r
]
creeper_face = [
   dg, g, lg, g, g, g, g, g,
   g, g, g, g, dg, lg, lg, g,
   lg, b, b, g, g, b, b, lg, 
   g, b, gr, lg, g, gr, b, g,
   g, dg, g, b, b, dg, g, g,
   lg, g, b, b, b, b, lg, dg,
   g, g, b, b, b, b, g, g,
   g, lg, b, dg, g, b, dg, lg
]
while True:
   sense.set_pixels(angry_face)
   sleep(3)
   sense.set_pixels(eggplant_not_face)
   sleep(3)
   sense.set_pixels(creeper_face)

   
   sleep (3)