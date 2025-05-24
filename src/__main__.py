import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import speaker
import lyrics
import splitter
import translator

SPEAKER_NAME = "atlas" # "gaia" | "atlas" | "uranos" | "conrado"
MAX_CONCURRENCY = 1 # Workers
SILENCE_BETWEEN = 2000 # Seconds
SPEED = 0.8 # 1 is normal

# Input
TEXT_INPUT= """
AUDIO SCRIPT FOR
HALF-LIFE

TRAIN RIDE
TRAIN VOICE (VOICE OVER)
Good morning and welcome to the Black Mesa Transit System. This automated train is provided for the security and convenience of employees of the Black Mesa Research Facility personnel. Please feel free to move about the train or simply sit back and enjoy the ride.
The time is 8:47 a.m. Current topside temperature is 93 degrees, with an estimated high of one hundred and five. The Black Mesa compound is maintained at a pleasant 68 degrees at all times.
This train is inbound from Level 3 dormitories to Sector C Test Labs and Control Facilities. If your intended destination is a high-security area beyond Sector C, you will need to return to the Central Transit hub in Area 9 and board a high-security train. If you have not yet submitted your identity to the retinal clearance system, you must report to Black Mesa Personnel for processing before you will be permitted into the high-security branch of the transit system.
Due to the high toxicity of material routinely handled in the Black Mesa compound, no smoking, eating, or drinking are permitted within the Black Mesa Transit System.
Please keep your limbs inside the train at all times. Do not attempt to open the doors until the train has come to a complete halt at the station platform. In the event of an emergency, passengers are to remain seated and await further instruction. If it is necessary to exit the train, disabled personnel should be evacuated first. Please stay away from electrified rails, and proceed to an emergency station until assistance arrives.
A reminder that the Black Mesa Hazard Course decathlon will commence this evening at nineteen hundred hours in the Level 3 facility. The semifinals for high-security personnel will be announced in a separate Secure Access transmission. Remember, more lives than your own may depend on your fitness.
Do you have a friend or relative who would make a valuable addition to the Black Mesa team? Immediate openings are available in the areas of Materials Handling and Low-Clearance Security. Please contact Black Mesa Personnel for further information. If you have an associate with a background in the areas of theoretical physics, biotechnology or other high-tech disciplines, please contact our Civilian Recruitment Division. The Black Mesa Research Facility is an Equal Opportunity Employer.
A reminder to all Black Mesa personnel: Regular radiation and biohazard screenings are a requirement of continued employment in the Black Mesa Research Facility. Missing a scheduled urinalysis or radiation check-up is grounds for immediate termination. If you feel you have been exposed to radioactive or other hazardous materials in the course of your duties, contact your Radiation Safety Officer immediately. Work safe, work smart. Your future depends on it.
As the train pulls into the final station:

TRAIN VOICE
Now arriving at Sector C Test Labs and Control Facilities.
As the security guard approaches the train to let you out.

TRAIN VOICE
Please stand back from the automated door and wait for the security officer to verify your identity. Before exiting the train, be sure to check your area for personal belongings. Thank you and have a very safe and productive day.
TRAIN RIDE - EXIT

Scene: A security guard (“Barney”) opens the door of your train:

BARNEY
Morning, Mr. Freeman. Looks like you’re running late?
ANOMALOUS MATERIALS
ANOMALOUS MATERIALS – LOBBY

Scene: Barney at reception desk.

BARNEY
Hey, Mr. Freeman—I had a bunch of messages for you, but we had a system crash about twenty minutes ago and I’m still trying to find my files. Just one of those days I guess. They were having some problems down in the test chamber, too, but I think that’s all straightened out. They told me to make sure you headed down there as soon as you got into your hazard suit.
Scene: If you press button under the reception desk an alarm goes off and guard chastizes you:

BARNEY
Come on, Gordon, you trying to get me into trouble?
Scene: Scientist sprints toward fax machine in corner if you push the button.

SCIENTIST
Get away from there, Freeman! I’m expecting an important message!
ANOMALOUS MATERIALS - LAB AIRLOCK

Scene: Security Guard turns you away from airlock door when you haven’t put on your hazard suit.

BARNEY
Sorry, Mr. Freeman, I’ve got explicit orders not to let you through without your hazard suit on.
Once you’ve put on your suit he says:

BARNEY
Go right on through, sir. Looks like you’re in the barrel today.
ANOMALOUS MATERIALS - LAB EXIT

Scene: Security Guard turns you away from door you’re not authorized to enter (beyond the conference rooms).

BARNEY
You’ve got the wrong airlock, Mr. Freeman. You know I can’t let you through here.
ANOMALOUS MATERIALS – COMPUTER ROOM

SCIENTIST 1
Good morning, Gordon.
SCIENTIST 2
Big day today, Freeman.
SCIENTIST 3
The sample was just delivered to the test chamber.
ANOMALOUS MATERIALS - TEST LAB CONTROL ROOM

Scene: Control room overlooking the Anomalous Materials Test Lab. Scientists in readiness for a critical test. They are urging you to get down to the lab.

SCIENTIST 1
Ah, Gordon, here you are. We just sent the sample down to the Test Chamber.
SCIENTIST 2
We’ve boosted the antimass spectrometer to 105 percent. Bit of a gamble, but we need the extra resolution.
SCIENTIST 3
The Administrator is very concerned that we get a conclusive analysis of today’s sample. I gather they went to some lengths to get it.
SCIENTIST 1
They’re waiting for you, Gordon. In the Test Chamber.
ANOMALOUS MATERIALS – HALLWAY BETWEEN CONTROL ROOM AND ELEVATOR

Two scientists run for controls on wall.

SCIENTIST 1
Quick! It’s about to go critical!
SCIENTIST 2
What the hell is going on with our equipment?
SCIENTIST 1
It wasn’t meant to do this in the first place!
ANOMALOUS MATERIALS - TEST CHAMBER AIRLOCK

Scene: Your final briefing before entering the test lab. Two scientists seal you in an airlock at the entrance to the lab and give you alternating warnings and encouragement.

SCIENTIST 1
I’m afraid we’ll be deviating a bit from standard analysis procedures today, Gordon.
SCIENTIST 2
Yes, but with good reason. This is a rare opportunity for us. This is the purest sample we’ve seen yet.
SCIENTIST 1
And potentially the most unstable!
SCIENTIST 2
Oh, if you follow standard insertion procedures, everything will be fine.
SCIENTIST 1
I don’t know how you can say that. Although I will admit that the possibility of a resonance cascade scenario is extremely unlikely, I remain uncomfortable with the---
SCIENTIST 2
Gordon doesn’t need to hear this. He’s a highly trained professional. We have assured the Administrator that nothing will go wrong.
SCIENTIST 1
Ah yes, you’re right. Gordon, we have complete confidence in you.
SCIENTIST 2
Well, go ahead. Let’s let him in now.
ANOMALOUS MATERIALS – TEST CHAMBER DISASTER

Scene: Player enters Test chamber from the airlock. All scientists voices are over the intercom (voice over).

SCIENTIST 2
Testing...testing... [cough...tap...feedback] Everything seems to be in order.
SCIENTIST 1
All right, Gordon, your suit should keep you comfortable through all this. The specimen will be delivered to you in a few moments. If you would be so good as to climb up and start the rotors, we can bring the antimass spectrometer to eighty percent and hold it there until the carrier arrives.
SCIENTIST 1
Gordon, are you not hearing me? Climb up and start the rotors, please.
SCIENTIST 1 (getting impatient)
Climb up and start the rotors.
SCIENTIST 1
Very good. We’ll take it from here.
SCIENTIST 2
Power to stage one emitters in three...two...one...
SCIENTIST 2
I’m seeing predictable phase arrays.
SCIENTIST 2
Stage two emitters activating...now.
SCIENTIST 1
I have just been informed that the sample is ready, Gordon. It should be coming up to you any moment now. Look to the delivery system for your specimen.
SCIENTIST 1
Standard insertion for a nonstandard specimen. Go ahead, Gordon. Slot the carrier into the analysis port.
SCIENTIST 2
Overhead capacitors to one oh five percent.
SCIENTIST 1
Gordon, we cannot predict how long the system can operate at this level, nor how long the reading will take. Please work as quickly as you can.
SCIENTIST 2
Uh...it’s probably not a problem...probably...but I’m showing a small discrepancy in...well, no, it’s well within acceptable bounds again. Sustaining sequence.
SCIENTIST 1
Nothing you need to worry about, Gordon. Go ahead.
Now the beam effects crackle out of control.

SCIENTIST 1
Gordon! Get away from the beams!
SCIENTIST 2
Shutting down. [beat] Attempting shut-down. It’s not...it’s not shutting down.
But they’re everywhere now, things crashing down, lights failing. A beam zaps the control booth.

SCREAMS.

UNFORESEEN CONSEQUENCES
UNFORESEEN CONSEQUENCES – BROKEN PLASMA TANK ROOM

Scene: After you come up from the broken test chamber, you meet two scientists outside the elevator. One sits on the ground shaking his head, in shock. The other is comforting him.

SCIENTIST 1
Why didn’t they listen!
SCIENTIST 2
We tried to warn them.
SCIENTIST 1
I never thought I’d see a resonance cascade, let alone create one.
The second scientist notices you.

SCIENTIST 2
Gordon, you’re alive! Thank God for that hazard suit. I’m afraid to move him, and all our phones are out. Please, get to the surface as soon as you can, and let someone know we’re stranded down here. You’ll need me to activate the retinal scanners. I’m sure the rest of the science team will gladly help you.
You’ll need me to activate the retinal scanners.
You lead the scientist to the retinal scanners; and he opens the control room door for you.

SCIENTIST 2
Be careful, Gordon.
UNFORESEEN CONSEQUENCES – TOP OF ELEVATOR

Scene: After the elevator crash, you climb up the shaft and come out in time to see Barney fighting a zombie.

BARNEY
Gordon! Man, am I glad to see you! What the hell are these things? And why are they wearing science team uniforms?
UNFORESEEN CONSEQUENCES – TRAIN PLATFORM

Scene: If you go back through the lobby and out onto the train platform where you came in, the catwalk creaks when you step on it.

SCIENTIST
No, stay back! Gordon!
[screams as he falls]
OFFICE COMPLEX
OFFICE COMPLEX -- BARNACLE LOUNGE

A scientists waits in the darkened room full of barnacles, just outside the elevator where you arrive in the office complex:

SCIENTIST
Gordon! If I’d known it was you, I’d have let you in! Everyone’s heading for the surface, but I think they’re crazy not to stay put. Someone is bound to come by and rescue us.
OFFICE COMPLEX – DARK OFFICE

Scientist shuts off lights as you pass his hiding place. If you go around to him, he says:

SCIENTIST
I’m not so sure I want to get to the surface. What if the world finds out what we were doing down here?
OFFICE COMPLEX —SCIENTIST IN A STAIRWELL

SCIENTIST
I just overheard a secure access transmission...soldiers have arrived and they’re coming to rescue us. Of course, I have my doubts that we’ll live long enough to greet them.
OFFICE COMPLEX – FINAL ELEVATOR SHAFT

Scene: Dangling scientist looses grip.

SCIENTIST
I...I can’t hold on much...longer...
OFFICE COMPLEX –CORRIDORS

Scene: Throughout the office complex, Security Guards helpfully urge you to seek higher ground.

BARNEY
Hey, what the hell are you doing down here? Get topside! I hear troops are coming in to save us.
BARNEY
Maybe help is on its way, but I’m not waiting around for it. We’ve got to get topside.
BARNEY
Don’t count on the cavalry finding us down here. Head for the surface.
BARNEY
Elevators are out of order...but we can still climb.
BARNEY
Word is, once we get to the surface, the military’s made arrangements for us.
“WE’VE GOT HOSTILES”
“WE’VE GOT HOSTILES” - SECURITY BOOTH

Scene: You step off an elevator into a high security storage area. To your left, a control/security booth is staffed by one security guard. Opposite the booth is a sealed silo door. A scientist pounds on the security booth, screaming at the guard:

SCIENTIST 1
For god’s sake, open the silo door! They’re coming for us; it’s our only way out!
The guard turns to the button that opens the silo door, and is attacked by a zombie which emerges from a vent behind him.

SCIENTIST 1
Oh my God...we’re doomed!
“WE’VE GOT HOSTILES” - EXECUTIONS

Scene: As you progress through the security storage area, you see various scientists running up to human soldiers. The scientist are relieved to see the “cavalry”—but their relief is short-lived. The soldiers simply execute them.

SCIENTIST
Rescued at last! Thank God you’re here!
Various Scientist Voices:

SCIENTIST
Don’t shoot! I’m with the science team!
SCIENTIST
Take me with you! I’m the one man who knows everything!
“WE’VE GOT HOSTILES” – OVERHEARD FROM AIRSHAFT

As you crawl over a soldier in the room below:

GRUNT
I killed twelve dumbass scientists and not one of ‘em fought back. This sucks.
“WE’VE GOT HOSTILES” – SILO DOOR CONTROL ROOM

After clambering through the airshafts, you come back into the control room where you can open the door into Silo D. The scientist hiding in the room speaks:

SCIENTIST
Well, so much for the government. Their idea of containment is to kill everyone associated with the project! Judging from your hazard suit, I’d say you were part of what went wrong—isn’t that right? Now look...if anyone can end this catastrophe, it’s the science team in the Lambda complex, at the opposite end of the base. With the transit system out, I couldn’t tell you how to get there. But there’s an old decommissioned rail system somewhere through here—beyond the silo complex. If you can make it through the rocket test labs, you might be able to worm your way through the old tunnels to track down whatever’s left of the Lambda team. You can trust them. You can trust all of us. Good luck.
BLAST PIT
BLAST PIT – INSIDE THE ROCKET SILO

Scene: Dying scientist pleads with you as you approach tentacle.

SCIENTIST
Fire the…rocket engine. Destroy the damned thing before it grows any larger!
BLAST PIT – TENTACLE SILO CONTROL ROOM

Scene: Audio for the scientist being grabbed by tentacle. Pure terror.

SCIENTIST
No...no... Get it off me! Get it off!
BLAST PIT – SILO CORRIDOR

Scene: You are creeping through corridors that surround the shell of a rocket-test silo which is inhabited by an immense tentacle with acute hearing. A Security Guard warns you to stay very quiet.

BARNEY
(whispering)
Be quiet! This thing hears us!
Scene: Another security guard, throwing caution to the wind, makes a desperate and noisy attack on the giant tentacle, firing his gun and charging at it.

BARNEY
(screaming)
Hey, over here! Eat lead, you outerspace octopus!
BLAST PIT –PATH TO POWER SILO

Scene: Scientist in corridor inspecting inactive power gauges. The guy doesn’t have a clue.

SCIENTIST
I hope no one expects me to start up the generator. Smithers went down there and never came back.
Scene: Scientist huddled atop power generator, hiding. He is fearful and yet irritated.

SCIENTIST
This is my hiding spot, and I’m not moving until the situation is drastically improved. Now go away and don’t tell anyone I’m here.
Scene: On the return trip, the scientist contemplates the working power meter in corridor.

SCIENTIST
Excellent! Someone has restored all power! We’ll have the engine up again in no time!
POWER UP
POWER UP - TRACK CONTROL ROOM

Scene: A security guard lies dying on the floor of a train track control room.

BARNEY
Mister, if you can get the power on, that train’ll take us straight to the surface. I would try it myself, but it’s a long way down to the generator room. And there’s…things in the way.
Scene: After you come back from switching on the power, if Barney still lives:

BARNEY
I’m never gonna make it...you better go on without me.
ON A RAIL
ON A RAIL – TRAIN TUNNELS

Scene: Security guard flags you down as you approach a track barrier.

BARNEY
Freeman, I've been waiting for you! One of your scientist pals said to give you a message. You’re supposed to take this old rail system up to some kind of satellite delivery rocket. I don’t know where it is exactly, and the old guy was so worried about getting out of here alive he didn’t tell me. The main thing is, the military aborted the launch, so when you do find the rocket, you'll have to get up to the control room and launch it yourself. He said something about a Lambda team needing the satellite in orbit if they were ever going to clean up this mess.
ON A RAIL – OUTSIDE, BEFORE THE ROCKET LAUNCH AREA

Scene: Two grunts are on patrol by the outdoor train tracks, somewhat relaxed, not expecting to be surprised from behind (which is where you overhear them).

GRUNT 1
So who is this guy Freeman?
GRUNT 2
He was at ground zero.
GRUNT 1
Science team? You think he was responsible? Sabotage, maybe?
GRUNT 2
Yeah, maybe. All I know for sure is, he’s been killing my buddies.
GRUNT 1
Oh yeah, he’ll pay. He will definitely pay.
ON A RAIL – OUTSIDE THE CONTROL ROOM

Scene: As you sneak past the dynamite charges, before entering the control room area, you can hear grunts talking beyond the door:

GRUNT
I didn’t sign on for this shit. Monsters, sure. But civilians? Who ordered this operation anyway?
APPREHENSION
APPREHENSION – ICHTHYOSAUR OBSERVATION ROOM

Scene: Scientist who witnessed Icky’s attack waits in the observation room above.

SCIENTIST
Did you see it? They said it was hauled from the Challenger Deep, but I’m positive that beast never swam in terrestrial waters until a week ago. There’s a tranquillizer gun in the shark cage, but I’m not sure it would work on this species. You’re welcome to try.
APPREHENSION – AIRLOCK BEFORE CRYOGENIC STORAGE AREA

SCIENTIST
Gordon Freeman—it is you, isn’t it? The science team has been tracking your progress with the Black Mesa security system. Unfortunately, so has the military. That suit of yours is full of tracking devices. Still, it’s better than going naked in this place. It’s cold in there and you’ll have to hurry. It could sap your suit power in a matter of moments. If you’re bent on reaching the Lambda complex, then you’ll want to keep to the older industrial areas, where the security system is full of holes. It’s worked for me so far.
APPREHENSION – ASSASSIN AREA

Scene: Barney awaits you with an urgent message, but the assassin kills him in mid-sentence.

BARNEY
Freeman, right? I’ve got a message for you. Make sure you don’t--- [deathsound]
APPREHENSION - AMBUSH SEQUENCE

Scene: You are jumped by a bunch of soldiers. They knock you unconscious. As you wake, you hear them talking, before they dump you in a trash compactor.

GRUNT
Get him. Heh, heh, nice hit. All right, we got him.
During the drag:

GRUNT 1
Where we taking this Freeman guy?
GRUNT 2
Topside. For questioning.
GRUNT 1
What the hell for? We got him. Let’s kill him now.
GRUNT 2
Uhhhh...and if they find the body?
GRUNT 1
Body? What body?
GRUNTS 1 & 2
(laughter)
QUESTIONABLE ETHICS
QUESTIONABLE ETHICS – APPROACH TO LOBBY

Scene: As you approach the lab lobby, Barney waits at a corner to clue you in:

BARNEY
Hey, it’s no good up there. It’s all sealed off. The only way out would be to find someone with scanner access who can open the front door. I’m pretty sure there’s a few scientists hiding somewhere in the labs. Maybe with both of us looking, we can track them down and get them to let us out.
QUESTIONABLE ETHICS – TAU CANNON LAB

Scene: As you approach a barricaded laser lab, you hear Barney and a scientist arguing, then the sound of the Tau cannon revving up. You break into the lab to find the Tau cannon smoldering in a pile of gibs.

BARNEY
What is this thing? Some kinda weapon?
SCIENTIST
Put that down—it’s a prototype.
We hear Barney fire the Tau cannon. It blasts through the wall where the player is walking.

BARNEY
Man! Why aren’t we using it?
SCIENTIST
It’s much too unpredictable. Don’t let it overcharge!
BARNEY
What do you mean, overcharge?
There is an explosion and SCREAMS. The barricade is blown away.

QUESTIONABLE ETHICS – SCIENTISTS IN HIDING

Scene: You have managed to break into a small storage area behind an out of control surgical robot. scientists are hiding in the storage closet. They ask for your help in getting free, and offer their own help (which you will need to get out of the labs).

SCIENTIST 1
A scientist, thank God! Get us out of here before those military drones figure out where we’re hiding!
SCIENTIST 2
We all have retinal scanner access. Escort us to the lobby, and we can get out of the lab.
SCIENTIST 3
You’ll have to shut down the surgical unit first. Peters switched it on but I’m afraid he never made it back.
QUESTIONABLE ETHICS – SUCCESSFUL EXIT

Scene: As the scientist works the scanner and lets you out of the labs.

SCIENTIST
Well, I’ll let you out, but I’m warning you...it’s hell out there. It’s completely under military control. You’ll have to sneak and fight your way from one end to the other, and I don’t expect you’ll meet many of our peers along the way. But if you do survive and somehow make it across the base, you’ll end up at the Lambda complex, where the rest of the science team has taken shelter. I wouldn’t venture there myself, but I will let them know that you are coming.
SURFACE TENSION
SURFACE TENSION – SNIPER ALLEY

Scene: Wounded security guard calls for help.

BARNEY
Help... Help me... Somebody please help me... I’m dying out here... Please help me...
SURFACE TENSION – BOOBY-TRAPPED BUILDING

Scene: Scientist holed up in a “closet” in a room which has been completely boobie-trapped. One false move and the whole place will go up.

SCIENTIST
You’re heading for the Lambda complex, aren’t you? I was heading there myself, until I wound up here and...well, simply lost my nerve. Take one look through that door and you’ll see what I mean. I’m just going to wait out the catastrophe in here. If you intend to go on, then I beg of you...proceed with extreme caution.
SURFACE TENSION – TACTICAL MAP

Scene: With Gargantua on your heels, you reach a map-table overlooking a sealed compound. There is a dead soldier sprawled by the table, and the voice of his commander crackles over an intercom:

COMMANDER (VO)
Come in, Cooper. Do you copy? Forget about Freeman. We’re abandoning the base. If you have any last bomb targets, mark them on the tactical map. Otherwise, get the hell out of there. Repeat, we are pulling out and commencing airstrikes. Give us targets or get below.
“FORGET ABOUT FREEMAN”
“FORGET ABOUT FREEMAN” – LOADING BAYS

Scene: As you enter the first area, near the parking lot, you hear a panicked warning coming over the radio.

GRUNT (VO)
Forget about Freeman. We are cutting our losses and pulling out. Anyone left down there now is on his own. Repeat, if you weren’t already, you are now ---
LAMBDA CORE
LAMBDA CORE – AFTER BATTLE WITH ALIEN GRUNTS

Scene: Scientist waits in sealed room beyond the assassin area.

SCIENTIST
I apologize, Mr. Freeman, but I couldn’t risk opening that door until I was sure you’d scoured the area. This is the last entrance to the Lambda Complex—every other has been sealed off to contain the invasion. When we realized that you might actually make it here, we drew straws to see who should stay behind to let you through. Obviously, I drew the short one. My colleagues are waiting at the tip of the Lambda reactor...waiting for you, I mean. The reactor is shut down right now, but you can activate it on your way up. You’ll have to flood the core anyway to get into the teleportation labs. You’re not authorized to know about those...but I can see you already know a great deal more than any one man is supposed to.
LAMBDA CORE – GLUON GUN TEST FIRING RANGE

Scene: Scientist in the gluon gun dispensary.

SCIENTIST
Were you in weapons research, too? I built the gluon gun, but I just can’t bring myself to use it on a living creature. You don’t look as if you have any trouble killing things.
LAMBDA CORE – IN COOLANT TANK OBSERVATION ROOM

Scene: Scientist in maintenance/coolant area reminds player to switch on both pumps.

SCIENTIST
Freeman, isn’t it? You’ll need to activate both pumps to flood the reactor, and then that access pipe down there will take you to the core. Time is short!
And if you’ve turned on the pumps:

SCIENTIST
Don’t linger, Mr. Freeman! You’ve turned on the pumps. Now take the access pipe, flood the core, and get on up to the labs without delay!
LAMBDA CORE – SURVEY TEAM EQUIPMENT ROOM

Scene: Barney and scientist waiting for you.

SCIENTIST
Gordon Freeman! You finally found us!
BARNEY
So this is the guy. We thought you’d never make it.
SCIENTIST
This is the supply depot for our first survey team. Quite a few handsome specimens were collected from the borderworld and brought back this way—uhh, before the survey members started being collected themselves, that is. We suspect there is an immense portal over there, created by the intense concentration of a single powerful being. You will know it when you see it. I hate to say this, Gordon, but you must kill it, if you can.
BARNEY
Yeah, you’d better kill it.
SCIENTIST
Of course, you owe us nothing, Mr. Freeman. But you’ve come this far. You know as much about these creatures as anyone.
BARNEY
Enough to know that if you don’t wipe it out, there won’t be much for you to come home to.
SCIENTIST
Yes. So...if you’re willing, my colleague is waiting for you at the main portal controls. He will open the gates for you, Mr. Freeman. Do hurry.
BARNEY
Don’t forget to gear up. And I’ll cover you while you’re waiting for that portal to warm up.
Scientist proceeds to unlock longjump module.

SCIENTIST
This, Mr. Freeman, is a long-jump module—created expressly for navigation in the world beyond. I certainly hope you received long-jump training, because once you’re in Xen you will need it. I would advise you to practice before crossing over.
LAMBDA CORE - MAIN PORTAL CONTROLS

Scene: A scientist waits at the control panel for the main portal. He speaks, and then gets busy over the controls, slowly opening the portal

When player enters main portal area:

SCIENTIST
Hello, Freeman—I’m up here. Practice your long-jump if you must, but hurry up!
30 seconds later:

SCIENTIST
All right, I can open the portal now. The process is complicated, and once it’s begun I must not be interrupted or I will have to start all over again. Don’t enter the beam until I give the okay, understood? I will begin.
When the beam is nearly active:

SCIENTIST
We’re almost there, Freeman. Get yourself in position.
When the beam is fully activated:

SCIENTIST
It’s ready! You must go! Now!
If player starts down ramp into portal too early:

SCIENTIST
Not yet, Freeman!
If player jumps into portal before it’s ready:

SCIENTIST
Freeman, you fool!
If player delays entering portal:

SCIENTIST
Hurry up, Freeman, I can’t keep it open forever!
ENDGAME
Scene: After destroying the Nihilanth, the Administrator waits for you:

ADMINISTRATOR
Gordon Freeman in the flesh. Or rather, in the hazard suit. I took the liberty of relieving you of your weapons; most of them were government property. As for the suit, I think you’ve earned it. The borderworld, Xen, is in our control for the time being, thanks to you. Quite a nasty piece of work you managed over there. I am impressed.
That’s why I’m here, Mr. Freeman. I have recommended your services to my employers, and they have authorized me to offer you a job. They agree with me that you have limitless potential.
You’ve proved yourself a decisive man, so I don’t expect you’ll have any trouble deciding what to do. If you’re interested, just step into the portal and I will take that as a yes.
Otherwise...well…I can offer you a battle you have no chance of winning. Rather an anticlimax, after what you’ve just survived.
The door of the train opens. A dimensional gate appears beyond.

ADMINISTRATOR
Time to choose.
If you hesitate:

ADMINISTRATOR
It’s time to choose.
If you step in, we fade into CREDITS. The Administrator speaks in voice-over:

ADMINISTRATOR
Wisely done, Mr. Freeman. I will see you up ahead.
If you don’t step in, the Administrator gives you about 10 seconds, then the door closes.

ADMINISTRATOR
Well, it looks like we won’t be working together.
ADMINISTRATOR
No regrets, Mr. Freeman.
You are teleported into the final bad place.

...THE END...
Hidden text
Deleted passages of text can be recovered in the document, revealing what appears to be an earlier version of the script which includes additional transcripts. These include a list of the major characters in the game, an outline for the original epilogue which takes place entirely on Earth (as opposed to the final sequence which teleports around Xen), and all of the individual speech lines from the scientists, security guards, and the Nihilanth.

Character list
CHARACTERS:

Scientists:

The scientists are brisk and businesslike; faced with the stress of fantastically improbable situations, they either devolve into hysterical panic and shock, or shield themselves with hyperrational analysis. They are your coworkers, mentors, and allies; although occasionally they are too busy to even notice you. When you are injured, they will inject healing agents, making them extremely important to your existence.

Barneys:

Barneys are base security guards. They are friendly, fearless, and practical allies. In a pinch, they will provide backup fire, attacking aliens and other human enemies.

Grunts:

Human military units sent in to “clean up” the base following the disaster. It is their job to execute anyone with knowledge of the research project that went awry. The more you know about the project, the more they want to kill you. They especially hate you, Gordon Freeman, personally—because you have cut down quite a few of through their buddies.

G-Man:

The cryptical bureaucrat, mystery man with a briefcase. He appears in the shadows, disappears when you chase him down dead-end corridors. He leads you into danger and guides you to safety, as the whim strikes him. His motives remain mysterious, but at the end of the game, when you have extinguished an alien civilization, he offers you a job with whoever it is he works for.

Original epilogue
NIHILANTH AUDIO

[nihilanth/nil_comes.wav]
...comes another...

C4A1 – C4A1a
[nil_last.wav]
...the last you are the last you are....

C4A1a – C4A1b
[nil_die]
...die you all die you all die....

C4A1b – C4A2
[nil_win.wav]
...win you cannot win...

C4A2 – C4A3
[nil_done.wav]
...done what have you done...

C4A3
To 2-Crystal Arena
[nil_thieves.wav]
...thieves you all are thieves you all are...

To Headcrab Arena
[nil_deceive.wav]
... deceive you will deceive you...

To Houndeye Arena
[nil_alone.wav]
...alone not you alone not you alone...

To Bullsquid Arena
[nil_now_die.wav]
...now die now die now...

To Vortigaunt Arena
[nil_thetruth.wav]
...the truth you can never know the truth...

To Alien Grunt Arena
[nil_slaves.wav]
...their slaves we are their slaves we are...

To Garguanta Arena
[nil_thelast.wav]
...the last I am the last...

To Place of Two Headcrabs
[nil_man_notman.wav]
... you are man he is not man for you he waits for you...

Deathblast
[nil_freeman.wav]
...Freeman...

DESERT (EPILOG)

Scene: After destroying the alien invasion portal, you teleport back to Earth. You find yourself in an administrative setting. There are high windows along one wall, through which you see a glimpse of terrestrial sky, and the other side is lined with locked doors. You can hear the idling noises of Xen masters, shock troopers, and vortigaunts behind those doors. The G-Man walks toward you. You have no weapons.

Gman_offer has been cut into several new pieces:

G-MAN [gman_offer.wav]
Gordon Freeman in the flesh. Or rather, in the hazard suit. I took the liberty of relieving you of your weapons; most of them were government property. As for the suit, I think you’ve earned it. The borderworld, Xen, is in our control for the time being, thanks to you. Quite a nasty piece of work you managed over there. I am impressed.

That’s why I’m here, Mr. Freeman. I have recommended your services to my employers, and they have authorized me to offer you a job. They agree with me that you have limitless potential.

You’ve proved yourself a decisive man, so I don’t expect you’ll have any trouble deciding what to do. If you’re interested, just step into the portal and I will take that as a yes.

Otherwise...well…I can offer you a battle you have no chance of winning. Rather an anticlimax, after what you’ve just survived.

Gman_offer has been cut into several new pieces:

G-MAN [gman_suit.wav]
Gordon Freeman in the flesh. Or rather, in the hazard suit. I took the liberty of relieving you of your weapons; most of them were government property. As for the suit, I think you’ve earned it.

GMAN [gman_nasty.wav]
The borderworld, Xen, is in our control for the time being, thanks to you. Quite a nasty piece of work you managed over there. I am impressed.

GMAN [gman_potential.wav]
That’s why I’m here, Mr. Freeman. I have recommended your services to my employers, and they have authorized me to offer you a job. They agree with me that you have limitless potential.

GMAN [gman_stepin.wav]
You’ve proved yourself a decisive man, so I don’t expect you’ll have any trouble deciding what to do. If you’re interested, just step into the portal and I will take that as a yes.

GMAN [gman_otherwise.wav]
Otherwise...well…I can offer you a battle you have no chance of winning. Rather an anticlimax, after what you’ve just survived.

He opens his briefcase. A dimensional gate glimmers within.

GMAN [gman_choose1.wav]
Time to choose.

G-MAN [gman_choose2.wav]
It’s time to choose.

If you step in, we fade into CREDITS. The G-MAN speaks in voice-over:

G-MAN [gman_wise.wav]
Wisely done, Mr. Freeman. I will see you up ahead.

If you don’t step in, the G-MAN gives you about 10 seconds, then shuts the briefcase.

GMAN [gman_wontwork]
Well, it looks like we won’t be working together.

G-MAN [gman_noregret.wav]
No regrets, Mr. Freeman.

He goes translucent, and disappears completely. As soon as he vanishes, the doors along the hall open nearby, and the last survivors of Xen come looking for you....
"""

def process_sentence(prefix, i, sentence, length):
    try:
        if not sentence.strip():
            return f"[skip] Empty sentence at {i}"

        dir = f"audios/{prefix}"
        os.makedirs(dir, exist_ok=True)

        base_filename = f"{dir}/{i:06d}"        

        speaker_path = f"samples/{SPEAKER_NAME}.wav"

        # Translated audio
        translated_file = f"{base_filename}_1_pt.mp3"
        translated = translator.translate(sentence)
        status_translated =  speaker.generate_tts(translated, translated_file, 'pt', speaker_path, SPEED, SILENCE_BETWEEN)
        lyrics.embed(translated, translated_file, 'por')

        # Main audio
        main_file = f"{base_filename}_2_en.mp3"
        status_main = speaker.generate_tts(sentence, main_file, 'en', speaker_path, SPEED, SILENCE_BETWEEN)
        lyrics.embed(sentence, main_file)
        
        return f"[done] prefix={prefix} progress={i}/{length} status=({status_translated}, {status_main})"
    except Exception as e:
        return f"[error] Frase {i+1} '{sentence}': {e}"

def process_all(prefix, sentences):
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENCY) as executor:
        futures = [executor.submit(process_sentence, prefix, i+1, s, len(sentences)) for i, s in enumerate(sentences)]
        for future in as_completed(futures):
            print(future.result())

def process_text(text, prefix):
    sentences = splitter.split_text_advanced(text)
    process_all(prefix, sentences)

process_text(TEXT_INPUT, f"halflife_{SPEAKER_NAME}")
