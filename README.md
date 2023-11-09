    Risk in python 

The objective of this project is to build a working clone of the popular board game risk.

Objective 1
Taken from another's initial code, I had to refactor it and implement my own logic and comments.
The initial code was ridden with overcomplicated naming conventions hard to read code, as it did not
have commented out information regarding what was happening. My initial objective was to parse through it
and add my own comments as I figured out what each class, object, and method were doing. 

Objective 2
My second objective was to take the authors initial idea of creating the map of Europe and to create a 
map of North America. I was able to implement the author's logic of using coordinates and create polygonic 
shapes that, when defined in a drawing method, created workable and viewable countries. I also created a "remove-list" 
where I removed certain smaller countries and Islands as to simplify the overall map. In the game's start up design, I created a 
method where when the game initialized, the maps were drawn onto the screen. Styling for different aspects of the game, such as the 
"Move", and "Attack" buttons were already given with the author's code.

Objective 3
Now that I had a map, I started to build the games logic. The first thing I did was create a method that implemented 
the dice rolling component of Risk. The dice method randomized the attacker's and defender's dice, as in the game Risk, where
the attacker has 3 dice and the defender has two. I used python's random method to randomly throw out 3 numbers, 1-6 for the attacker 
and 2 numbers, 1-6, for the defender. Later on in the code, I linked the dice method to the Roll Dice button, which I created after 
building the roll dice method, and inside the terminal you can see the outcomes of the randomized dice rolling.

Objective 4
The next objective that was handled was to create a Hover method when a country was hovered, the country's information was shown in a
smaller text area and displayed the number of units. I also created a + and - button, which is not yet functional but the idea is that during
the "Place Units" phase, a player can increment and decrement units on the specified country. Currently, the player can increment and decrement armies
by clicking on the country itself but in the future, I will look to change where the increment and decrement methods can be called.

The current state of the game is stable but limited functionality. The game can be initialized and the map is drawn and you can add armies to your 
controlled countries. The Phase button and Roll dice functions are working but the logic for moving units has not yet been implemented. My next objective 
is to be able to execute an attack between two countries which will require me to define what an attack country is and what a defending country is.