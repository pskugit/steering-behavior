# Steering behavior
> a study on emergent behavior of simple force controlled agents

This is a small showcase of steering behaviors realized in python with pygame. 
It was inspired by Daniel Schiffman's "Autonomous Agents and Steering - The Nature of Code" [https://www.youtube.com/watch?v=JIz2L4tn5kM] which is in turnbased on Craig Reynolds article on "Steering Behaviors For Autonomous Characters" [http://www.red3d.com/cwr/steer/]

## Prerequisites

To run main.py, the only additional libraries needed are pygame and numpy

```
$ pip install pygame
$ pip install numpy 
```

## Usage

![](/images/sb.gif?raw=true "Optional Title")

The agents are capable of a whole range of steering behaviors.
The basics are:
- seek: steer towards an (x,y) point
- flee: steer away from an (x,y) point
- arrive: steer towards an (x,y) point and avoid overshoot

The more complex ones:
- separate: flees from adjacent agents
- align: aligns direction with adjacent agents
- cohesion: seeks adjacent agents

When combining the latter three, flocking behavior can emerge as showcased above.

![](/images/sb1.png?raw=true "Optional Title")

## Meta

Philipp Skudlik 

[https://github.com/pskugit](https://github.com/pskugit/)

