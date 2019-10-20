# Digitized Circles #
*by Robert Kuramshin*

## Installation: ##
Installation From Source:
- install [python 3](https://www.python.org/download/releases/3.0/)
- install dependencies `pip3 install -e .`


## Part 1: ##
Usage:
- Click at the desired center of circe and drag to change size
- Release mouse button to set circle size
- To create a new circle simply click anywhere on the screen again
- To exit press escape

Visuals Explanation:
- Blue circle signifies the bounds of the drawn circle
- Grid circles will be highlighted blue as a digitized representation of the blue circle
- Two red circles will show maximum and minimum circles formed by the selected blue circles

Algorithms:  
`biggest circle` - The biggest circle formed by the points is selected by iteratively attempting to create circles with a larger radius until any of the previously overllaped points are not longer interesected.   
`smallest circle` - A similar algorithm to the biggest circle is implemented here. Instead of incrementing the circle radius, the radius is decreased until the circle fails to intersect the same points.
`circle intersection` - To determine which grid circle will interesect the user selected circle I compared the distance between the circles to their radii.
`circle radii`

## Part 2: ##
Usage:
- Click any grid circle to select it (it will change color from gray to blue)
- Once desired circles are selected, click the gray box in the bottom right color to generate circle
- A blue circle will appear that will attempt to fit the selected points

Visuals Explanation:
- Blue grid circles are selected, gray are not selected
- The blue circle will represent the attempt to draw a circle that best fits the selected points
- To exit press escape

Algorithms:  
`fit circle` 
