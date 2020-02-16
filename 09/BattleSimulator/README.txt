Author: herealways (here_always) (herealways996) (Morty Li), You can find me on Github (herealways)!

This Program simulates two monsters fight aginst each other.
Hopes you enjoy it!

Help:
First we need to choose 2 competitors.
1-5 Choose competitor 1 (e.g. Press 1 to choose Warrior).
6,7,8,9,0 Choose competitor 2 (e.g. Press 7 to choose Slime).
You can rechoose competitors before the fight.

After choosing Competitors:
Press F let them fight against each other!
If any of the competitors is defeated, his image will become "X".

When the fight ends:
Press Q to quit.
If you want to watch another fight, then:
Press C to clean the screen.
Choose competitors again, and press F.

Known issue:
In prolonged battle (Warrior vs. Warrior), the program will end with heap overflow.


About this game:
I get the idea of the game's fighting system from a very classic game named "Magic Tower".
(I don't know if I translated it correctly, you can Google "魔塔" to see if you know this game)

Basically, it is turn based fight. Competitor 1 will attack competitor 2, and competitor 2 attack competitor 1.
When one competitor is under attack, His health = health - damage
The fight will end when one of the competitor's health <=0, and the living competitor wins the fight.

Every monster has health, attack, and defense.
Damage that one competitor deals to another = His attack - His opponent's defense
If His opponent's defense >= His attack, then damage = 1


Monsters' data:
MonsterCode	Name		Health    Attack	Defense
1/6			Warrior		100		  10		10
2/7			Slime		40		  20  		2
3/8			RockySlime  20		  16		16
4/9			Skeleton	25		  55		0
5/0			BigSlime	250		  12		0

Make a custom monster:
You can add custom monster to this game! Here is an example: (this example has been added to the code)
1. Define the monster's image using projects/09/BitmapEditor/BitmapEditor.html. Then copy the function into DrawMonster class and rename it like "function void drawNEW_MONSTER(int location)".
2. Set a monsterCode for the new monster, for example: 10. Then add this code into DrawMonster.drawCompetitor(): if (monsterCode = 10) {do DrawMonster.drawNEW_MONSTER(location);}
3. In BattleSimulator.run(), bind a key to choose this monster as competitor, and set the NEW_MONSTER's data.
For example, bind Z to Choose NEW_MONSTER as competitor1, X to choose NEW_MONSTER as competitor2, the NEW_MONSTER has 666 health, 22 attack, 11 defense:
if (key = 90) { let competitor1 = Monster.new("NEW_MONSTER", 666, 22, 11, 10, 100, 1);}
if (key = 88) { let competitor2 = Monster.new("NEW_MONSTER", 666, 22, 11, 10, 200, 2);}

help: Monster.new() takes 6 parameters: name, health, attack, defense, location, order
	  For competitor1, location should be 100, and order should be 1.
	  For competitor2, location should be 200, and order should be 2.
	  You are responsible to make sure the new key do not collide with existing key!
4. Save the code, and use Z or X to use your new monster!