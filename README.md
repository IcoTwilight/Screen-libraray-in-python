# Screen libraray in python
*A simple customizable CMD for python. The current source code is very very messy and I am only releasing a compiled version of the program.*

*I will release a 2.0 version with full customization at some point next year(2022) and that will contain the source code for both.*

## **Known bugs:**

#### *the time and screen will only update when an ask, say or clear is called.*
#### *Trying to use another file and naming it consolla.ttf will  result in the text being very odd.*

## **DOCS**:

### How to install:
Put the .pyc file into the same folder as your project and simply import it. You will also need the consolla.ttf file to be in the same folder as the .pyc for it to work.

### Print Hello, world
```
import screen
screen.say("Hello, world")
```

### Get user input
```
import screen
name = screen.ask("What is your name> ")
```

### Clear the screen
```
import screen
screen.clear()
```

### Quit
```
import screen
screen.quit()
```


##### Credit to [blit text function](https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame) for the blit_text function used in the engine
