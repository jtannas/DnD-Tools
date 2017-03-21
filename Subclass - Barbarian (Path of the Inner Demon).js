/*  -WHAT IS THIS?-
	The script featured here is made as an optional addition to "MPMB's Character Record Sheet" found at http://flapkan.com/mpmb/dmsguild
	You can add the content to the Character Sheet's functionality by adding the script below in the "Add Custom Script" dialogue.

	-KEEP IN MIND-
	Note that you can add as many custom codes as you want, but you have to add the code in at once (i.e. copy all the code into a single, long file and copy that into the sheet).
	It is recommended to enter the code in a fresh sheet before adding any other information.
*/

/*	-INFORMATION-
	Subject:	Subclass (a.k.a. Archetype)
	Effect:		This script adds a subclass for the Barbarian, called "Path of the Inner Demon"
					This is taken from the DMs Guild Website (http://www.dmsguild.com/product/186273/)
					The source copy was taken on 2017-03-18
	Code by:	Joel Tannas
	Date:		2017-03-20
	Sheet:		v12.87
	
	Please support the creator of this content (Aric Eckart) by downloading the source pdf from DMs Guild
*/

ClassSubList["inner demon"] = {

	regExpSearch : /^(?=.*Demonic)(?=.*Rager).*$/i,
	
	subname : "Path of the Inner Demon",
	
	fullname : "Demonic Rager",
	
	source : ["DMguild", 186273],
	
	features : {
		"subclassfeature3" : {
			name : "Dark Fury",
			source : ["DMguild", 186273],
			minlevel : 3,
			description : "\n   " + "While raging, I gain resistance to fire damage and have advantage on saving throws against spells and other magical effects",
			eval : "AddResistance(\"Fire (in rage)\");",
			save : "Adv. vs spells and magical effects in rage;",
			removeeval : "RemoveResistance(\"Fire (in rage)\");"
		},
		"subclassfeature6" : {
			name : "Fiendish Hunger",
			source : ["DMguild", 186273],
			minlevel : 6,
			description : "\n   " + "When I reduce a creature to 0 hp with a melee attack, I gain temporary hit points equal to my Constitution modifier + my Barbarian Level (minimum of 1)"
		},
		"subclassfeature10" : {
			name : "Blood Offering",
			source : ["DMguild", 186273],
			minlevel : 10,
			description : "\n   " + "While raging, I can use an action to take 1d10 slashing damage (unreduceable) in order to summon lesser demons."
						+ "\n   " + "The demons appear in unoccupied spaces within 20ft, roll initiative as a group, and each demon stays until my rage ends or until it drops to 0 hit points. " 
						+ "There is a limit of 8 demons, and the total of their challenge ratings may not exceed 2. "
						+ "The demons are friendly to me and my companions, and obey any verbal command I issue them. "
						+ "If I give no commands, they defend themselves from hostile creatures but otherwise take no actions. ",
			eval : "AddAction(\"action\", \"Blood Offering (while raging)\", \"barbarian\");",
			removeeval : "RemoveAction(\"action\", \"Blood Offering (while raging)\");",
			recovery : "long rest",
			usages : 1
		},
		"subclassfeature14" : {
			name : "Fiendish Mutation",
			source : ["DMguild", 186273],
			minlevel : 14,
			description : "\n   " + "When I enter a rage, roll once on the demonic mutation table. Until that rage ends, I gain the effect rolled and am considered a fiend."
		},
	}
}

ClassList["barbarian"].subclasses[1].push("inner demon");