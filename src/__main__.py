import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import speaker
import lyrics
import splitter
import translator

NAME = "RE3_delayed"
SPEAKER_NAME = "atlas" # "gaia" | "atlas" | "uranos" | "conrado"
MAX_CONCURRENCY = 1 # Workers
SILENCE_LEFT = 1000 # Seconds
SILENCE_RIGHT = 2000 # Seconds
SPEED = 0.75 # 1 is normal

# Input
TEXT_INPUT= """
1. Raccoon City’s Narrator
(Screen: A picture of the Umbrella Corporation’s logo)
Jill Valentine (Narration):  It all began as an ordinary day in September... 
An ordinary day in Raccoon City, a city controlled by Umbrella.
 (Screen: Jill Valentine’s upper body moving from left-to-right)
Jill Valentine:  No one dared to opposed them... and that lack of strength 
would ultimately lead to their destruction. I suppose they had to suffer the 
consequences for their actions, but there would be no forgiveness.
 (Screen: Jill closes her eyes)
Jill Valentine:  If only they had the courage to fight. It’s true once the 
wheels of justice began to turn, nothing can stop them. Nothing.
 (Screen: Jill sitting on a bed, legs crossed, and loading a gun.)
Jill Valentine:  It was Raccoon City’s last chance... and my last chance... 
My last escape.

2. Defenses Crushed
(Screen: Racoon City Streets. A helicopter flies in the distance)
Pilot of Helicopter: this is Chopper Delta. Prepare to drop off at Area 
E95070...
 (Screen: People are screaming and running from the horde of zombies coming 
their way as the helicopter flew by.)
 (Screen:  A zombie rears it’s head and yelled. Zombies attack a car with a 
woman inside screaming.)
 (Screen: A man watches zombies attack a person)
Man: What are they?! (turns to his right to see a zombie coming after him) 
No!
 (Screen: Raccoon City Police arrive in their cars, creating a barrier as 
they moved into position and police rush out of a police van.)
 (Screen:  A helicopter hovers by a clock tower as soldiers slide down on 
ropes.)
(Screen:  The Raccoon City Police officers are situated behind their squad 
cars.)
Officer 1:  Blockade is ready. Awaiting orders.  Over. (Officers aim their 
guns)
Radio:  All units proceed to Richmond and Victoria...
Soldier 1:  Alright, let’s do it.
Soldier 2: Go, go, go!
 (Screen:  The Raccoon City Police officers are situated behind their squad 
cars, guns aimed at the zombies.)
Officer 2: Fire!
 (Screen: The Raccoon City Police officers fire at the zombies.)
Officer 3: Come and get it!
 (Screen:  The zombies continue to advance, no matter how many times they are 
shot. Zombies fall to the ground, only to get back up again.)
Officer 4: Son of a!
Officer 5: Don’t give up!
 (Screen:  The zombies reach the officers and attack. The officers scream.)
 (Screen:  An elevator chimes as two soldiers walk by, the Umbrella 
Corporation logo on their vests.)
Soldier 3: Where are they?
 (Screen:  They turn as the elevator door opens, revealing zombies coming 
out.)
Solider 4: Where did they come from?!
 (Screen:  Outside, soldiers are ambushed by zombies as they fire at them. A 
soldier takes out a grenade.)
Soldier 5: (pulls the pin off of grenade) Die!
 (Screen:  The soldier tosses the grenade and it explodes, but the zombies 
are barely fazed by it.)
 (Screen:  A soldier is surrounded by zombies as he backs away and fires his 
automatic gun at them.)
Soldier 6: You want some more?! (His back hits the wall.)
 (Screen:  The zombies reach for him and he screams.)
 (Screen:  The police barricade is deserted and the camera closes in on a 
police helmet, the visor down to reflect zombies passing by.)
 
3. The Escape
 (Screen:  The screen is black as words appear:  Farewell to my life. 
Farewell to my home. This is my last chance for survival. This is, my last 
escape.)
 (Screen: An explosion occurs at the entrance of a building. Zombies are 
thrown back as Jill Valentine rolls out of the building.)
 
4. Surrounded
 (Screen:  Jill Valentine finds herself surrounded by zombies. She backs into 
a door and bashes into it with her shoulder. She breaks in after the second 
time and backs away from the advancing zombies, turning around and running. 
She opens a door and goes inside.)

5. Choice
 (Screen: Black)
Jill Valentine: September Twenty-Eight, Daylight... The monsters have 
overtaken the city. Somehow... I’m still alive.
 (Screen:  Jill is standing before a small stairway, a man named Dario is 
behind her.)
Jill Valentine: Okay. (turns around) We gotta get out of here.
Dario: (shock and hysterical) Wha? What do you think you’re talking about?! I 
just lost my daughter out there! How dare you tell me to go back outside!
Jill Valentine: I’m sorry about your daughter. But there isn’t going to be 
any rescue! We have to get out of here!
Dario: (yells) NO!! I’m not going anywhere! I rather starve myself than be 
eaten by one of those undead monsters! Now leave me alone!
 Screen: Dario runs into the back of a truck trailer and locks himself 
inside. Jill Valentine tries talking to him again.) 
Dario: Told you! I’m not leaving! Never! Just leave me be!

6. Get Away!
 (Screen: Jill Valentine enters a bar through the back door. She hears 
grunting and sees Brad Vickers being attacked by a zombie, whom he pushes 
away.)
Brad Vickers: Get away! (fires his gun at it)

7. No Escape
 (Screen: After Jill Valentine helps Brad Vickers kill the zombie, Brad 
Vickers falls into his behind. Jill Valentine walks up to him.)
Jill Valentine: Brad, hang in there. Why isn’t someone doing something about 
this?
Brad Vickers: I didn’t know you sere still alive, Jill. The police aren’t 
trained for this kind of situation. What could they do? (stands up) Listen, 
he’s coming for us. We’re both gonna die!
 (Screen: Brad Vickers turns away.)
Jill Valentine: What are you saying?
Brad Vickers: You’ll see. (walks to the door) He’s after S.T.A.R.S. members. 
There’s no escape.
 (Screen: Brad Vickers leaves the bar.)

8. End of Brad Vickers
 (Screen: Jill Valentine walks up to the Raccoon Police Station when she 
hears a noise. She turns around and gasps.
Brad Vickers: (hunched and bleeding) J-Jill!
Jill Valentine: Brad!
 (Screen: A creature in black, Nemesis, jumps between them and Brad Vickers 
screams, falling onto his behind.)
Brad Vickers (crawling backwards as Nemesis advances) Jill! Help! (Nemesis 
grabs him by the neck and lifts him up) Noooooooooo!
 (Screen: A purple tentacle from Nemesis’ wrist shoots out and pierces Brad 
Vickers in the neck.)
Jill Valentine: No!
 (Screen: Nemesis tosses Brad Vick’s body onto the ground as Jill Valentine 
gasps, staring at her fallen comrade.)
Jill Valentine: Brad...?
Nemesis: S.T.A.R.S.

9. Outside
 (Screen: Jill Valentine walks away from the entrance doors when suddenly, 
the doors thrust forward, but remain lock Jill Valentine moves back.)

10. Radio Transmission
 (Screen: Jill Valentine was about to leave the S.T.A.R.S. office when the 
radio beeps. She walks over to it.)
Man’s Voice:...No...Come...head...Our platoon is...off...No survivors have 
been found...This is Carlos...se-...poi-...immediately...

11. Meet Carlos(Restaurant)
 (Screen: Jill Valentine opens the hatch to the basement when she hears a 
noise. She turns around to see a mercenary, Carlos Oliviera, sitting on his 
behind while holding onto the counter.)
Jill Valentine: What’s that?
Carlos Oliviera (stands up): Calm down, lady. I’m no zombie. My name is 
Carlos, corporal of Umbrella’s Biohazard Counter Measure Force. What’s your 
name?
 (Screen: Carlos Oliviera walks up to Jill Valentine.)
Jill Valentine: Jill. Did you just say you belong to Umbrella’s army?
Carlos Oliviera: Yeah. We came all the way out here to save your civilians, 
but the mission went bad the minute we landed.
 (Screen: A door slams and Nemesis roars, charging from the back.)
Jill Valentine: No. How did he find me?

12. Basement (If you choose ‘Run into the basement’)
 (Screen: Jill Valentine kneels before the hatch.)
Jill Valentine: This way!
 (Screen: Jill Valentine and Carlos Oliviera jump into the basement, which 
was flooded with a foot of water. Nemesis bangs around above, knocking a few 
pipes loose that began to fill the basement with water. Jill Valentine and 
Carlos Oliviera escape through a ventilation shaft.)
Jill Valentine: Wait. I have to ask you something.
Carlos Oliviera: I know. You wanna ask me out. All the foxy ladies have my 
accent. It drives them crazy.
Jill Valentine: What? Keep dreaming. Tell me, why did Umbrella send your team 
in?
Carlos Oliviera: We’re here to rescue the civilians.
Jill Valentine: Don’t lie to me! Umbrella is the reason why this whole mess 
began! 
Carlos Oliviera: Look, we’re just mercenaries. Hired hands. You really think 
the master would tell his dog why he has to retrieve the stick he just threw? 
If you want answers, you should talk to someone else. I am not with Umbrella.
 (Screen: Zombies appear behind Jill Valentine.)
Carlos Oliviera: We have to finish this later. Believe it or not, we’re only 
here to rescue the civilians. If you can trust me, then help us! Think about 
it!
 (Screen: Carlos Oliviera runs away.)

13. Kitchen (If you choose ‘Hide inside the kitchen’)
 (Screen: Jill Valentine runs to the counter.)
Jill Valentine: Over here!
 (Screen: Jill Valentine and Carlos Oliviera hide behind the counter as 
Nemesis roars where they once stood. Jill Valentine grabs and oil-based lamp 
and throws it into the kitchen, hitting the leaking pipes. Jill Valentine and 
Carlos Oliviera hide under the counter as the kitchen explodes.)
Carlos Oliviera (Jill Valentine and Carlos Oliviera stand): Are you crazy?! 
You could’ve barbeque both of us!
 (Screen: Jill Valentine and Carlos Oliviera head for the entrance door as 
Nemesis stands up, roaring. Jill Valentine and Carlos Oliviera leave, Carlos 
Oliviera firing at Nemesis.)
Jill Valentine (Carlos Oliviera walking off): I need to ask you something. 
Why did Umbrella send your team here?
Carlos Oliviera (turns around): Our mission is to rescue the civilians.
Jill Valentine: How kind of you. Considering that Umbrella caused all this in 
the first place, those liars!
Carlos Oliviera: Look, we’re just mercenaries. Hired hands. 
 (Screen: Jill Valentine and Carlos Oliviera hear glass breaking.)
Carlos Oliviera: No time for talking. If you can believe me, then join us. 
Think about it! 
 (Screen: Carlos Oliviera runs off.)

14. Meet Carlos(Raccoon Press)
 (Screen: Jill Valentine enters an office and finds a mercenary, Carlos 
Oliviera, lying on the ground near a fire. She walks up to Carlos Oliviera 
and kneels before him.)
Jill Valentine: Hey.
Carlos Oliviera (moans): Wha...where am I? (sits up with hand to head)
Jill Valentine: Relax. You’re fine.
Carlos Oliviera: If you say so, but my head feels like it’s about to explode. 
(stands with one arm around his stomach) Anyway, name’s Carlos. Glad to meet 
you, lady.
Jill Valentine: Jill. (Carlos Oliviera walks to the doorway) Alpha Team. 
R.P.D. S.T.A.R.S. Unit. Who do you represent?
Carlos Oliviera (enters the hallway and points gun forward while whistling) 
S.T.A.R.S.? I see. Well, I’m a member of the Biohazard Counter Measure Force 
sent by Umbrella Corporation. (lowers gun)
Jill Valentine: Sent by Umbrella?
Carlos Oliviera (turns to Jill Valentine) Hey, don’t look at me like that! 
What did I say? D’you have a problem?
 (Screen: Jill Valentine and Carlos Oliviera hear Nemesis walking up the 
burning stairs.)
Jill Valentine: Oh no! It’s him!

15. Hide (If you choose ‘Hide in the back’)
 (Screen: Jill Valentine and Carlos Oliviera hide in the office under a 
window. Nemesis walks around the hallway until an explosion knocks him 
through the window, knocking him out. Jill Valentine and Carlos Oliviera 
leave the Raccoon Press.)
Jill Valentine: I need to ask you something. Why did Umbrella send your team 
here?
Carlos Oliviera: Our mission is to rescue the civilians.
Jill Valentine: How kind of you. Considering Umbrella caused all this in the 
first place, those liars!
Carlos Oliviera: Look, we’re just mercenaries. Hired hands. Do you really 
think the master would tell his dog why he would have to retrieve the stick 
he just threw?
 (Screen: Jill Valentine and Carlos Oliviera hear glass breaking.)
Carlos Oliviera: No time for talking. If you can believe me, then join us. 
Think about it! 
 (Screen: Carlos Oliviera runs off.)

16. Window (If you choose ‘Jump out of the window’)
Jill Valentine: Come on!
 Screen: Jill Valentine and Carlos Oliviera jump through the window in the 
back as something explodes behind them, falling into a heap of garbage 
below.)
Carlos Oliviera: Ow! That kill! (Jill Valentine and Carlos Oliviera stand up) 
Just so you know, I’m not into that ‘Pain is Pleasure’ thing, okay?
Jill Valentine: Just deal with it. That thing wants me dead. We gotta get out 
of here!
 (Screen: Jill Valentine and Carlos Oliviera go through the door and are 
outside Raccon Press. Jill Valentine wipes her forehead as Carlos Oliviera 
begins to leave.)
Jill Valentine: Wait. (Carlos Oliviera stops) I have to ask you something.
Carlos Oliviera: I know. You wanna ask me out. All the foxy ladies have my 
accent. It drives them crazy. (Jill Valentine and Carlos Oliviera walk a 
bit.)
Jill Valentine (stops walking): I have to know. Why did Umbrella send you 
here?
Carlos Oliviera (turns around): Because, we’re on a civilian rescue mission.
Jill Valentine (walks up to Carlos Oliviera): Oh, you’re full of it! They’re 
the ones who caused all of this in the first place!
Carlos Oliviera: Look, we’re just mercenaries. Hired hands. You really think 
the master would tell his dog why he has to retrieve the stick he just threw? 
 (Screen: Jill Valentine doesn’t answer.)
Carlos Oliviera: Listen, if you want answers about Umbrella, you’re asking 
the wrong guy. Believe it or not, we’re only here to rescue civilians. If you 
can trust me, join us. Think about it!
 (Carlos Oliviera runs off.)

17. The Mercenaries
 (Screen: Jill Valentine enters a trolley and a mercenary with white hair, 
Nicholai Ginovaef, walks up to her.)
Jill Valentine: You’re one of the survivors from the rescue team, right? I 
just ran into your teammate, Carlos.
Nicholai Ginovaef: How did a girl like you managed to survive?
Jill Valentine: Hey, I’m no ordinary civy. I’m a member of S.T.A.R.S.
Nicholai Ginovaef: S.T.A.R.S.? You mean the R.P.D. special force team? (Turns 
and walks into the next car)
 (Screen:  A mercenary lying on the chairs, Mikhail Victor, moans as he 
clutches his arm, injured.)
Jill Valentine: Hey, is someone wounded back there?
 (Screen: Jill Valentine walks up to Mikhail Victor and kneels before him, 
inspecting his wounds.)
Jill Valentine: Oh, this looks bad.
Mikhail Victor (groaning in his sleep): They’re coming. Get ready! (raises 
his arm) Aaaaaah...vile...vile! (arm drops) Stand together!
Jill Valentine: Calm down. You’re safe now. (places her hand on his arm) 
Everything’s going to be okay.

18. The Plan
 (Screen: Jill Valentine enters the second car, where Nicholai Ginovaef and 
Carlos Oliviera are.
Carlos Oliviera: So Jill, you decide to help us out? It looks like we’re the 
only ones who survived. We should work together.
Nicholai Ginovaef: No. We can’t trust her.
 (Screen: Jill Valentine walks up a bit and Carlos Oliviera walks up to 
Nicholai Ginovaef)
Carlos Oliviera: Why? But Sergeant, we need her help! Our unit’s down to you, 
me, and Lieutenant Mikhail. That’s it! And Mikhail’s hurt bad. If we don’t 
cooperate, we won’t be walking away from this mission.
 (Screen:  Nicholai Ginovaef places a hand to his chin and pauses.)
Nicholai Ginovaef (places hand down): Hmm, fine. Then let’s go over our plan. 
We’re moving to the Clock Tower area, which is the designated landing zone 
for the extraction chopper. Once we get there, and give the signal, the 
chopper will fly in and pull us out.
Carlos Oliviera: That’s a lot of ground to cover. I don’t think we can make 
it on foot.
Nicholai Ginovaef: The main problem we have is the landing zone is cut off 
from here by the fire. So, we have no choice but to use this cable car to 
navigate through it. Fortunately, we can use it as a moving shield to get us 
through the worst areas.
Carlos Oliviera: That works for me. Good plan, sir!
Nicholai Ginovaef: Okay people, let’s get moving!
 (Screen: Nicholai Ginovaef leaves)
Carlos Oliviera (handing Jill Valentine something): Jill, put this on.
 (Screen: Screen turns black as sounds are heard. Screen changes to Jill 
Valentine wearing a utilities belt and alone.)

19. Trapped
 (Screen: Jill Valentine leaves the room of the electrical plant to see 
zombies outside the gate, pounding against it.)

20. Target (If you choose ‘Head to the emergency exit’)
 (Screen: Jill Valentine runs for the emergency exit, only to find it rusted 
shut. She runs to another door and unlocks it, going outside. Zombies are 
coming towards her when suddenly, an explosion knocks them back. Jill 
Valentine turns to see Nemesis on a rooftop, aiming his rocket launcher at 
her. She runs back inside as he fires off more rockets, killing the zombies.)

21. Electrocute (If you choose ‘Increase electrical output’)
 (Screen: Jill Valentine runs to the consol and presses a button. The 
electrical device becomes surrounded with electricity that shot out at the 
gate. The zombies are electrocuted until they explode. The electrical device 
gives off smoke as it stops.)

22. Firefighter Jill
 (Screen: Jill Valentine hooks up the fire hose to the water main and sprays 
water onto the fire, putting it out.

23. Umbrella Business Building (If you met Carlos at the Restaurant)
 (Screen: Jill Valentine enters the building)
Voice: Wait!
 (Screen: Jill Valentine hears gunshots and she runs inside to find Nicholai 
Ginovaef kneeling before the dead body of a mercenary, a laptop in his hand.)
Jill Valentine: What did you do?!
Nicholai Ginovaef: I had no choice. He was about to turn into a zombie. It 
would’ve been a threat, so I eliminated it. (begins working on his laptop)
Jill Valentine: But...he was still conscious, wasn’t it? 
Nicholai Ginovaef: He was as good as dead...and it took fewer bullets to kill 
him now than it would have if he had transformed.
 (Screen: Jill Valentine tries talking to him again.)
NIcholai Ginovaef (waves laptop): Not now! I’m busy!
 (Screen: Jill Valentine reads some files, then turns on the TV. A lady walks 
up to a product on the screen and Jill Valentine uses the product’s name as a 
password on the computer. The password is accepted and a door unlocks. Jill 
Valentine enters the room and collects the items inside, then goes to leave.)
 (Screen: Outside, zombies are slowly making their way to the Umbrella 
Business Building. They burst through the window, some getting caught up in 
the blinds before sliding in.)
 (Screen: At the door, Nicholai screams. The zombies open the door and walk 
in, heading for Jill Valentine.)

24. Umbrella Business Building (If you met Carlos at Raccoon Press Building 
and choose to jump out the window)
 (Screen: Jill Valentine walks into the building)
Voice: No! 
 (Screen: Jill Valentine hears something falls and runs in. Carlos Olivera is 
standing before a badly-injured mercenary that is sitting on the floor.)
Carlos Oliviera: Don’t make me do this, Murphy! I don’t want to shoot you!
Murphy (stands and slowly walks to Carlos Oliviera): Kill me! I...finished. 
Not...human...
Carlos Oliviera (walks back): Wait! We...we don’t have to do this!
Murphy: Please hurry...before I lose conscious...before it’s too late... Kill 
me!!
 (Screen: Carlos Oliviera screams as he fires his assault gun, killing 
Murphy. Murphy falls to the floor, dead. Carlos Oliviera falls to his knees 
onto the floor.)
Carlos Oliviera: ...Murphy...(hits the floor with his fist) Why...no, no... 
(get up and runs)
Jill Valentine: Carlos!
 (Screen: Carlos leaves the building. Jill Valentine reads some files, then 
turns on the TV. A lady walks up to a product on the screen and Jill 
Valentine uses the product’s name as a password on the computer. The password 
is accepted and a door unlocks. Jill Valentine enters the room and collects 
the items inside, then goes to leave.)
 (Screen: Outside, zombies are slowly making their way to the Umbrella 
Business Building. They burst through the window, some getting caught up in 
the blinds before sliding in.)
 (Screen: The zombies open the door and walk in, heading for Jill Valentine.)

25. Nemesis Cut-Off
 (Screen: Jill Valentine heads to the door past the water main when Nemesis 
walks in, roaring. Nemesis charges forward and raises a fist at Jill 
Valentine. She dodges the punch, Nemesis cutting through the water main and 
Jill Valentine steps backwards as he raises and arm, roaring.)


26. Falling
 (Screen: Jill Valentine runs through the garage when the area began to 
shake. She stops and looks around when suddenly, the ground falls out under 
her. Jill Valentine grabs the ledge in time and pulls herself up. To her 
horror, boxes from a van begin sliding out.

27. Climb (if you choose ‘Climb Up’)
 (Screen: Jill Valentine quickly climbs up and back away as the boxes slid 
and fell into the hole.)

28. Fall (if you choose ‘Jump Off’)
 (Screen: Jill Valentine yells as she falls down into the hole. Getting up 
from her knees, she jumps back as the boxes fell where she landed.)

29. Last One Standing
 (Screen: Jill Valentine opens the door leading to the trolley, hearing gun 
shots. Mikhail Victor is fighting against zombies, backing up into the far 
wall. Jill Valentine runs to help.)
 (Screen: Mikhail holds his side for a minute before continuing to fire.)
Mikhail Victor: Don’t come any closer!
 (Screen: Mikhail knocks the barrel towards them and fires, the barrel 
exploding and taking out the zombies (If there is no barrel, he uses a 
grenade to destroy the zombies). Mikhail Victor falls to his knees as Jill 
Valentine runs up to him.)
Jill Valentine: Mikhail, do you have some kind of death wish? 
Mikhail Victor: My people...they were wiped out by these monsters! I can’t 
stop just because I’m wounded!
Jill Valentine: But can’t you see those monsters are also the victims of 
Umbrella?
Mikhail Victor: Are you accusing me of taking it out on them? You don’t seem 
to understand something. We’re not really involve with the company! (tries to 
stand, but falls onto his behind) There’s no reason for any of us to take 
responsibility for this mess!
 (Screen: Jill Valentine takes Mikhail Victor’s arm and lifts him back up 
onto his feet, his arm around her shoulder.)
Jill Valentine: I know that...and right now, that’s the only reason why I’m 
trying to cooperate with you.
 (Screen: Jill Valentine helps Mikhail Victor into the trolley and back onto 
the seats.)
Mikhail Victor (holding his arm): I’m...sorry. I feel so useless.
Jill Valentine: Don’t. You fought hard and have the wounds to prove it.
Mikhail Victor (looks away): But...I’m still...alive. My men aren’t...
Jill Valentine: Don’t think about that now. Just rest.

30. Gas Station (If you met Carlos at Raccoon Press Building and jumped 
through the window)
(Screen: Jill enters the gas station. She walks up to the counter, then turns 
when she hears someone come in. Nicholai Ginovaef walks up to her.)
Nicholai Ginovaef: I’ll check over there.
 (Screen: Nicholai Ginovaef walks into the garage and begins inspecting the 
area. Jill Valentine finds and electronic lock and cracks the code, 
collecting the item inside. As she was about to leave the counter, sparks 
from a cut wire fly and hit the oil on the ground where Nicholai Ginovaef was 
kneeling, who screams as he stands up when the room explodes.)
Jill Valentine: Nicholai!
 (Screen: Jill Valentine tries to run to his aid, but dodges the wave of 
flames rushing out of the room. She gets up to see the gas station on fire 
and runs for the door, looking back one last time before leaving.)
 (Screen: Fire continues to engulf the gas station. Jill Valentine turns back 
to see small explosion, holding up her arms with a cry as she runs. The gas 
station finally explodes, sending Jill Valentine flying and screaming. She 
slowly gets up and leaves.)

31. Gas Station (Any other scenario except for above)
(Screen: Jill enters the gas station. She walks up to the counter, then turns 
when she hears someone come in.)
Carlos Oliviera: Jill!
 (Screen: Jill Valentine and Carlos Oliviera hear moaning outside)
Carlos Oliviera: Hey, the zombies are getting restless.
Jill Valentine: I know. I can hear them. What’s going on?!
 (Screen: Jill Valentine tries to go behind the counter.)
Carlos Oliviera (looking outside): Jill! 
Jill Valentine (turns around): What’s wrong?!
 (Screen: Zombies are walking towards the gas station.)
Carlos Oliviera: They’re coming! They must’ve sniffed us out! They know we’re 
here!
 (Screen: Jill Valentine raises an arm.)
Jill Valentine: Hey, calm down.
Carlos Oliviera (turning around and cocking his gun): Any objections to my 
playing hero this time?
Jill Valentine: What are you doing?!
 (Screen: Carlos Oliviera turns and leaves the gas station.)
Jill Valentine: Carlos!
 (Screen: Jill Valentine looks outside the glad door. Carlos Oliviera is 
firing at the advancing zombies.)
Carlos Oliviera: Eat this! (yells)
 (Screen: Jill Valentine runs behind the counter and cracks the code to the 
electronic lock. She collects the item inside, then turns to leave the 
counter.)
 (Screen: Sparks fly from a cut wire, causing the garage to explode. Jill 
Valentine dodges the wave of fire that came out, setting the gas station on 
fire. She runs for the door, looking at the garage one last time fore going 
outside. Carlos Oliviera is leaning against the gas station on his rear, 
appearing unconscious.)
Jill Valentine: Carlos! (falls to her knees) No!
Carlos Oliviera (takes a breath and looks at her): Relax. I’m not dead yet.
Jill Valentine: Are you okay? (stands up)
Carlos Oliviera (pants as he stand up, one arm around his middle): I’m fine. 
Huh, that hero stuff is harder than it looks.
 (Screen: They run away from the gas station)
(Screen: Fire continues to engulf the gas station. Jill Valentine turns back 
to see small explosion, holding up her arms with a cry as she runs. The gas 
station finally explodes, sending Jill Valentine flying and screaming. She 
and Carlos Oliviera slowly get up.)
Carlos Oliviera: Ouch. My ears are ringing. We both should be deaf by now. 
Olay, I’m gonna scrounge some equipment. There might not be any at our 
destination.
 (Screen: Carlos Oliviera leaves)

32. The Worm
 (Screen: Jill Valentine is running through the park when the area starts 
shaking again. She stops, then yells as the ground gives way. Jill Valentine 
falls into a sewer, standing up as she hears noises. She looks at the wall 
behind her, then walks backwards as the wall burst, a creature with four 
fangs and a large mouth bursting through to try and bite her before going 
back into the wall.)

33. Time to Go (If you met Carlos at Umbrella Office Building)
 (Screen: Jill Valentine fixes the trolley and stands just as Carlos Oliviera 
walks in.) 
Jill Valentine: Carlos, I’m sorry about Murphy, but there was nothing you 
could have done.
Carlos Oliviera: Yeah...You’re right, Jill. I’ll operate the cable car.
Jill Valentine: Uh...Nicholai...won’t be joining us. C’mon, let’s go.

34. Time to Go (Any other scenario except for above)
(Screen: Jill Valentine fixes the trolley and stands just as Carlos Oliviera 
walks in.) 
Carlos Oliviera: It looks like we’re ready to go. Here, take this. (hands 
Jill Valentine an item)
Jill Valentine: Okay. Uh...Nicholai...won’t be joining us.
Carlos Oliviera: I understand. I’ll operate the cable car. Let’s go.

35. Stowaway
 (Screen: Jill Valentine walks up to Carlos Oliviera as he works the controls 
for the trolley.)
Carlos Oliviera: It’s looking good. 
 (Screen: Carlos Oliviera pulls a lever and the trolley begins moving. 
Suddenly, the trolley shakes with the sound of an explosion, Jill Valentine 
crying out. They also hear someone yelling in pain.)
Carlos Oliviera: Mikhail!
 (Screen: Jill Valentine leaves the car and finds Mikhail Victor on the 
floor, leaning against the wall next to the door.)
Jill Valentine: Mikhail!
 (Screen: Jill Valentine turns to see Nemesis rising up, roaring.)

36. Sacrifice
 (Screen: Jill Valentine knocks Nemesis onto the floor, but Nemesis rises up 
again with a roar.
Mikhail Victor (standing up and aiming his gun): Jill, get out of the cable 
car now!
Jill Valentine: Mikhail, wait! Don’t!
Mikhail Victor (firing his gun): There’s no time! Hurry!
 (Screen: Jill Valentine leaves.)

37. The Last Stand
 (Screen: Mikahil Victor is firing at Nemesis while backing up, Nemesis 
advancing towards him.)
Mikhail Victor: Come one! Come on!
 (Screen: Mikhail Victor’s gun runs out of bullets and Nemesis knocks him 
into the side windows and he falls onto the seats. Mikhail Victor reaches for 
his gun, but Nemesis grabs him and throws him onto the floor, stomach first.)
Mikhail Victor (reaching into his vest) Just...a little closer...
 (Screen:  Nemesis raises a hand, a tentacle shooting out of his wrist as he 
walks to Mikhail Victor, who rolls onto his back to reveal a grenade.)
Mikhail Victor: You lose... (pulls the pin)
 (Screen: The trolley is wracked with explosions, and Nemesis’ body is thrown 
out the back window on fire. The screen turns black.)
Jill Valentine: Mikhail...
 (Screen:  The trolley is out of control and on fire. Jill Valentine stands 
up and walks to Carlos Oliviera, who is fiddling with a lever.)
Carlos Oliviera: No! The brakes are out!
 (Screen:  The trolley shakes and Jill Valentine and Carlos Oliveria cry out 
and move back a bit)

38. Window (If you choose ‘Jump out the window’)
 (Screen:  Jill Valentine runs to the window in the back of the trolley.)
Jill Valentine: It’s useless!
Carlos Oliviera (Jill jumps out the window): No!
 (Screen:  The trolley runs out of control and collides with the concrete 
gate and side of the Clock Tower.)
 (Screen:  Jill Valentine moans as she slowly stands up, finding herself in a 
bedroom that the trolley collided into. As she heads for the door, she hears 
something and turns around.)
 (Screen:  Zombies are moaning as they appear out of the fire next to the 
trolley.)

39. Brake (If you choose ‘Use the emergency brake’.)
 (Screen:  Jill Valentine runs up to the panel as Carlos Oliviera jumps out 
of the trolley.)
Jill Valentine: It must be...
 (Screen: Jill Valentine smashes her fist into the emergency break and cries 
out, one hand to her face.)
(Screen:  The trolley runs out of control and collides with the concrete gate 
and side of the Clock Tower.)
 (Screen:  Jill Valentine moan and stands up, finding herself in front of the 
Clock Tower outside the trolley.)

40. Just a Piece of Paper (If you choose ‘Use the emergency brake’.)
 (Screen:  Jill Valentine finds Carlos Oliviera in the dining room, his back 
to her.)
Jill Valentine: Carlos. I don’t believe it. You’re alive.
Carlos Oliviera: I’m not sure how we are gonna get out of this town.
Jill Valentine: What are you thinking about? We made it!
Carlos Oliviera (turns around): You don’t get it! They have no intention of 
letting us make it back alive! Do you really think we can trust their ‘great 
evacuation plan’? Huh! It’s just a piece of paper!
Jill Valentine: We don’t have any other choice than to trust them right now.
Carlos Oliviera: No! If we’re gonna die, then we should get to choose when it 
happens!
 (Screen:  Pause.)
 (Screen: Jill Valentine slaps Carlos Oliviera in the face, who cries out.)
Jill Valentine: So that’s it then, huh? You’re giving up?
Carlos Oliviera: No...I just...I can’t handle it!
 Screen:  Carlos Oliviera runs off.)

41. Nemesis Arrives
 (Screen: Jill Valentine heads for the door when Nemesis opens it, walking 
onto the balcony.) 
 Nemesis: S.T.A.R.S...(Roars)

42. Light (If you choose ‘Use the light’.)
 (Screen: Jill Valentine runs to the switch and turns on the light. Nemesis 
cries out and waves his arms around, blind. Jill Valentine dodges the arms 
and pushes Nemesis off the balcony.)

43. Cord
 (Screen:  Jill Valentine runs to the spotlight and rips out an electric 
cord. She tosses it into the puddle the Nemesis is standing in, electrocuting 
him. Nemesis yells, then collapses.  Jill Valentine heads for the door as 
Nemesis regains consciousness, roaring.)

44. Transport Cut-Off
 (Screen:  The Clock Tower bells are ringing as a helicopter appears, Jill 
Valentine exiting the Clock Tower.)
Jill Valentine: We’re saved. (waves arms) Down here!
 (Screen:  The helicopter prepares to land.)
Jill Valentine: It’s finally over...
 (Screen: A rocket launcher fires a rocket.)
Jill Valentine (sees the rocket): Huh? No!
 (Screen:  The rocket destroys the helicopter, Jill Valentine crying out as 
she held her head in her hands. The helicopter’s remains fall onto the exit 
of the Clock Tower, blocking her escape.)
Jill Valentine: No... (sees Nemesis with rocket launcher)

45. Infection
 (Screen:  Nemesis jumps down in front of Jill Valentine, trying to punch 
her. Jill Valentine dodges and moves back, but Nemesis thrusts his right arm 
forward, a tentacle shooting out and hitting her in the shoulder. Jill 
Valentine grunts as the tentacle pierces her shoulder, purple fluid seeping 
out of her wound.)

46. Help (If you choose ‘Use the emergency brake’.)
Carlos Oliviera: Jill!
 (Screen:  Carlos Oliviera jumps over the destroyed helicopter and begins 
firing at Nemesis. Nemesis fires a rocket, which explodes behind Carlos 
Oliviera and knocks him to the ground. Carlos Oliviera slowly gets back up 
and fires with a war cry. Nemesis aims the rocket launcher, but Carlos 
Oliviera does so as well, making it explode and knocking Nemesis back. Carlos 
Oliviera passes out.)

47. Nemesis Rises (If you or Carlos Oliviera destroy Nemesis’ rocket 
launcher.)
 (Screen:  Nemesis rise up with a roar, his jacket in tatters. He slowly 
walks over to Jill Valentine.)

48. Nemesis Falls
 (Screen: Nemesis is crying out as he bleeds heavily. He slowly walks into 
the destroyed helicopter, falling into the fire.)

49. Carlos...
Jill Valentine (walking over to Carlos Oliviera slowly): Carlos...
 (Screen:  Jill Valentine collapses with a moan of pain. Carlos Oliviera 
slowly regains consciousness and sees Jill Valentine.)
Carlos Oliviera: Jill! (Gets up slowly with one arm around his stomach and 
kneels before her, lifting her into his arms) Jill...(Shakes her a bit) Hey, 
don’t die on me. (holds Jill Valentine to him)
 (Screen: Screen fades to black.)
Carlos Oliviera: Jill! JIIIIIIIILLLLLL!!!!

50. Alone
 (Screen:  Jill Valentine walks slowly for a bit before collapsing.)
 (Screen:  Carlos Oliviera jumps over the destroyed helicopter and sees Jill 
Valentine.)
Carlos Oliviera: Jill! (runs over and lifts Jill Valentine into his arms) 
Jill, hang in there! (shakes Jill Valentine a bit) What have I done? I’m 
sorry Jill. (holds Jill Valentine to him) Please, wake up!
 (Screen:  Screen fades to black.)
Carlos Oliviera: Jill! JIIIIIIIILLLLLL!!!!

51. Chapel
 (Screen: Black.)
Jill Valentine: October First. Night. I woke up to the sound of falling rain. 
I can’t believe I’m still...alive.
 (Screen: Carlos Oliviera is kneeling before Jill Valentine, who is lying on 
a table in the chapel. Jill Valentine slowly comes to with a moan of pain.)
Jill Valentine: Carlos...?
Carlos Oliviera: It looks like our roles have been reversed from when we 
originally met, huh? Don’t worry, Jill. This chapel is safe.
Jill Valentine: ...I’ve been infected by the virus...haven’t I? (winces in 
pain)
Carlos Oliviera: Hey, take it easy.
Jill Valentine: I’m okay. I don’t...feel any pain. (rolls to her side away 
from Carlos Oliviera as he stands) But that’s what bothers me. If I can’t 
feel anything, then what does that mean?
Carlos Oliviera: Don’t give up, Jill. I’ll take care of you! Whatever you do, 
don’t let that virus beat you!
 (If you try to talk to Jill Valentine again.)
 (Screen: Carlos kneels before Jill Valentine.)
Jill Valentine: If I turn into a zombie...don’t hesitate. I want your 
word...that you’ll kill me...

52. Hunter
 (Screen:  Carlos Oliviera walks to the door leading to an office when he 
hears moaning. A zombie walks over from a corner. A screech is heard and a 
hunter lands, cutting off the zombie’s head. The hunter screeches at Carlos 
Oliviera.)

53. Traitor
 (Screen:  Carlos Oliviera enters an office.)
Voice: Don’t shoot! (sound of gunshots) Nooo!
 (Screen: Carlos Oliviera runs around a filing case to find Nicholai Ginovaef 
shooting at a mercenary.)
Carlos Oliviera: Nicholai?! You’re still alive?! (walks up to Nicholai 
Ginovaef)
Nicholai GInovaef: You saw what happened?
Carlos Oliviera: What’s going on?!
Nicholai Ginovaef: I’m one of the supervisors. That’s all you need to know. 
(aims gun at Carlos Oliviera)
Carlos Oliviera: Wait!
 (The mercenary pulls out a grenade and takes out the pin. Carlos Olivier and 
Nicholai Ginovaef runs, Carlos Oliviera running to the side as Nicholai 
Ginovaef is thrown out a window by the explosion.)

54. Enter Gamma
 (Screen:  Carlos Oliviera was about to leave the lab when the gammas in the 
test tubes bang on the glass, cracking it before throwing themselves at the 
test tubes, destroying them and freeing themselves.)

55. Bomb
 (Screen:  Carlos Oliviera enters the lobby and finds a bomb strapped to a 
pillar.)
Narration: It seems to be a time-based bomb.
 (Screen: Carlos Oliviera exits the hospital.)
 (Screen: Carlos Oliviera runs as the timer winds down.)
Carlos Oliviera: Come on!
 (Screen: The hospital explodes, Carlos Oliviera crying out as he flew into 
the air and rolls onto the ground. Carlos Oliviera leans against a pole, 
wiping the sweat from his brow with a sigh.)

56. Noises
 (Screen:  Carlos Oliviera enters the Clock Tower, hearing noises above and 
seeing the ceiling crack.)

57. Nemesis Returns
 (Screen: Carlos Oliviera runs through the folly when he hears noises. A part 
of the wall on the second floor cracks, then explodes. Nemesis, shirtless and 
with more tentacles on his right arm, jumps into the folly, roaring at Carlos 
Oliviera.)

58. Vaccination
 (Screen: Carlos Oliviera enters the chapel and walks up to Jill Valentine, 
kneeling before her. The screen turns black and Jill moans painfully.)

59. Bad News (If you meet Nicholai Ginovaef at the gas station and if you 
choose ‘Escape through the window’.)
 (Screen: Carlos is kneeling before Jill Valentine as she turns her head to 
look at him.)
Carlos Oliviera: We barely made it. How do you feel?
Jill Valentine (sits up): I’m okay. What happened to you?
Carlos Oliviera: I just fought with that monster. Uh...I’ve got some bad 
news. Nicholai’s still alive.
Jill Valentine: But I thought he was dead!
Carlos Oliviera: Heh, that guy doesn’t know the meaning of the word dead.
Jill Valentine: What is he after?!
Carlos Oliveria: I don’t know. All I know is that he is our enemy. I’m sorry 
Jill, but there is something I gotta take care of. (turns) I promise I’ll 
meet up with you later.
 (Carlos Oliviera runs off as Jill Valentine stands)

60. Playing (If you meet Carlos at the gas station.)
 (Screen:  Carlos Oliviera is kneeling before Jill Valentine.)
Carlos Oliviera (stands up): Hey, are you okay?
Jill Valentine (sits up): Yes...barely. What’s going on?
Carlos Oliviera: No way! That monster just doesn’t give up!
Jill Valentine: What? I thought we killed that thing!
Carlos Oliviera: No. It’s been waiting for you!
 (Screen:  Jill Valentine and Carlos Oliviera looked up as Nemesis roars.)
Jill Valentine: He’s playing with us. Carlos, do you think that it’s 
unstoppable?
Carlos Oliviera: No...I don’t think so. I’m sorry Jill, but I gotta go take 
care of a few things. Oh, and...bad news. Nicholai is still alive.
Jill Valentine: Nicholai? Are you sure?
Carlos Oliviera: Yes. I don’t know how, but I do know that he is our enemy. 
(turns) Remember, don’t trust him!
 (Screen: Carlos Oliviera runs off as Jill Valentine stands.)

61. Barge
 (Screen:  Jill Valentine leaves the chapel and enters the music room. She 
heads for the door when something bangs on it. Nemesis breaks the door off 
its hinges with a roar, going after Jill Valentine.)

62. Message
 (Screen: Jill Valentine is about to leave the secret room when the radio in 
the back beeps. She walks up to the radio.)
Radio: All supervisors. Mission terminated. Return immediately. Repeat:  All 
supervisors return immediately. Over.

63. Another Mutant
 (Screen: Jill Valentine leaves the secret room and is back in the cabin.)
Nicholai Ginovaef (walks up to Jill Valentine): I’m quite impressed you 
managed to stay alive up until now.
Jill Valentine: And you seem to be doing a pretty good job at looking after 
yourself. How about helping out?
Nicholai Ginovaef: I have no intention of helping you.
Jill Valentine: Because we’re nothing but pawns in all of this?
Nicholai Ginovaef: In a manner of speaking, you are. Our employers want 
detailed analysis of the zombie beings, which were created through infection 
by the T-virus.
Jill Valentine: You’re saying that they deliberately sent in a military unit 
to be butchered by their creations?
Nicholai Ginovaef: Note exactly. Although the conditions encountered on this 
operation were extreme, it was...an unexpected outcome that the team would 
be...wiped out. We were only required to collect live data from the subjects.
 (Screen:  The cabin begins to shake.)
Nicholai Ginovaef: Another mutant! (Runs off)

64. The Worm
 (Screen:  Jill Valentine leaves the cabin and runs. The graveyard shakes and 
Jill Valentine yells.)
Jill Valentine: What’s going on?! Whoa!
 (Screen:  the ground under Jill Valentine rises up as something moves 
underground. Jill Valentine gasps and screams as the ground under her feet 
falls and she lands in a trench. A pale-colored worm-like creature bursts 
from the ground, rising tall.)
Jill Valentine: What’s that?!
 (Screen:  The worm opens its mouth, revealing four long fangs and circular 
rows of teeth.)

65. The Escape
 (Screen:  Jill Valentine defeats the worm, who screeches, then dissolves. A 
piece of a fence falls, giving Jill Valentine a way to escape.)

66. Bridge Terror
 (Screen:  Jill Valentine rungs onto a wooden bridge, but then turns around 
as she hears a sound. A purple tentacle shoots out of the wooden plank in 
front of her.)
Jill Valentine (walking backwards as more tentacles shoot out) No...
 (Screen: A tentacle wraps around a metal support bar as Jill Valentine turns 
and runs. Nemesis uses the tentacle to jump onto the bridge, cutting Jill 
Valentine off.)

67. Push (If you choose ‘Push him off’)
 (Screen: Jill Valentine dodges Nemesis as he tries to swipe at her. She 
moves to his side and pushes him off.)

68. Missile (If you choose ‘Push him off’)
 (Screen:  Jill Valentine enters a small office to find Carlos Oliviera 
leaning on his arms on a table.)
Jill Valentine: Carlos...
Carlos Oliviera: Jill, listen very carefully. They’re planning on launching a 
missile directly into the city as soon as day breaks. The explosion will be 
powerful enough to destroy everything!
Jill Valentine: Are you sure about that?
Carlos Oliviera: Positive. I heard it from a supervisor.
Jill Valentine: They’ll go this far to cover their tracks? 
Carlos Oliviera: Come on. We have to hurry. There isn’t much time left!
 (Screen:  Carlos Oliviera leaves.)

69. Jump (If you choose ‘Jump off’)
 (Screen:  Jill Valentine dodges Nemesis as he tries to swipe at her. She 
yells as she jumps off the bridge and into the water below.)
 (Screen:  Nemesis roars, then walks to the dead factory.)

70. Job
 (Screen:  Jill Valentine jumps into a water walkway and begins running. 
Suddenly, zombies rise out of the water and surround her. Jill Valentine 
walks backwards into a wall and aims.)
 (Screen:  The zombies are killed by a onslaught of gun fire. Jill Valentine 
looks to see that it was Carlos Oliviera.)
Carlos Oliviera: Rescuing you is becoming a full-time job. (walks up to Jill 
Valentine.)
Jill Valentine: Thanks Carlos. I owe you one.
Carlos Oliviera: Listen closely Jill. They’re going to launch a missile 
directly into the city as soon as day breaks.
Jill Valentine: At dawn? B-but that’s only-
Carlos Oliviera: I know. We don’t have much time left. We have to split up 
and find a way out of here. And hey, (takes Jill Valentine’s cheek into his 
hand) watch out for that traitor Nicholai.
 (Carlos Oliviera runs off.)

71. Sneak (If you choose ‘Jump off’)
 (Screen:  Jill Valentine enters the entrance hallway. She was about to turn 
a corner when someone shoots at her and she hides behind the corner. Nicholai 
chuckles as he walks off.)
Jill Valentine: Nicholai?
 (Screen:  The shutter closes behind Nicolai Ginovaef.)

72. Bonus (If you choose ‘Push him off’)
 (Screen: Jill Valentine runs for the door to the garbage disposal room when 
suddenly, someone shoots at her. She takes cover behind a wall.)
Nicholai Ginovaef (hiding behind another wall): You’re still wandering 
around.
Jill Valentine: Nicholai? So, you wanna get out of here alone. Is that your 
plan?
Nicholai Ginovaef: I made certain that none of the other supervisors 
survived. Since I’’ be the only one who knows what really happened, I’ll have 
more...bargaining power when it comes to discussing my bonus. (fires at Jill 
Valentine, who hides.)
Jill Valentine: Then why kill me? I’m not on their payroll.
Nicholai Ginovaef (fires twice): Well, they want you eliminated for reasons 
of their own. The amount is modest, but there is a reward to be claimed upon 
the confirmation of your death.
Jill Valentine: That’s great! Except I have no intention in contributing to 
your retirement fund!
 (Screen:  Nicholai Ginovaef continues to fire until a tentacle wraps around 
his neck. Nicholai Ginovaef yells in pain as he was pulled up, blood pooling 
onto the ground where he once stood. When no more was heard, Jill Valentine 
walks over to where Nicholai Ginovaef once was.)
 (Screen:  Jill Valentine looks up in horror to see Nicholai Ginovaef hanging 
in the pipes of the ceiling, dead.)

73. Garbage Disposal
 (Screen:  Jill Valentine enters the garbage disposal room, which was dark.)
Announcement: Warning. Proceeding with Operation Number Thirteen. (door 
locks) Please evacuate immediately.
 (Screen:  The lights flicker on as Jill Valentine stares at the door, then 
turns around when she hears heavy footsteps.)
Nemesis (walking on garbage pile): S.T.A.R.S...(roars)
 (Screen:  Nemesis jumps down and swipes at Jill Valentine, who back away and 
dodges. Jill Valentine turns to run, but Nemesis cuts her off. Jill Valentine 
stands under a pipe and dodges another swipe, running away as the tentacles 
hit a valve. Nemesis thrashes about as he is covered in a stream of acid, 
which burns off some of his tentacles.)

74. Acid Death
 (Screen:  Nemesis falls apart from the acid eating at him. The garbage 
disposal room shakes and a key card falls out of a dead scientist’ coat 
pocket.)

75. Garbage Dump
 (Screen:  Red lights are flashing as the garbage disposal room’s floor 
splits in two, all of the garbage and Nemesis’ body sliding into a piqued 
pools below.)
 (Screen: Jill Valentine was moving away from the door to the garbage 
disposal room when the alarms go off.)
Announcement: Warning. Missile attack confirmed. All personnel evacuate 
immediately.

76. Garbage?
 (Screen:  Jill Valentine enters the control room and the screen show a pool 
of liquid below and what appears to be flesh-color garbage.)

77. Radio Room 1 (If you choose ‘Push him off’)
 (Screen:  Jill Valentine enters the radio room as the radio beeps.)
Carlos Oliviera: Jill...Jill, where are you? If you can hear this 
transmission, respond immediately!
 (Screen:  Jill Valentine runs up to the radio and presses a button.)
Jill Valentine: I’m here. What’s up?
Carlos Oliviera: I got us a ride. The chopper engines are running and ready 
to go.
Jill Valentine: On my way.
Carlos Oliviera: This city is about to become Ground Zero. Hurry up! And 
don’t forget to take that device with you!
 (Screen:  Jill Valentine turns to look at a portable device on the radio 
consol.)
Jill Valentine: What does it do?
Carlos Oliviera: that device tracks the distance of the approaching missile. 
Make sure you bring it with you. Now listen. Don’t give up We’re both gonna 
survive this! Just get over there!
 (Screen:  Jill Valentine grabs the portable device and was about to leave.)
Announcement: Warning. Missile attack confirmed. Warning missile attack 
confirmed. Emergency Level B. All personnel evacuate immediately.
 (Screen:  The shutters slide down and a panel opens up, revealing a ladder.)

78. Radio Room 1 (If you choose ‘Jump off’)
 (Screen: Jill Valentine enters the radio room and looks around. As she was 
about to leave, the radio beeps and she presses a button.)
Nicholai Ginovaef (helicopter sounds): You’re still alive. Such persistence.
Jill Valentine: Nicholai?
Nicholai Ginovaef: Sorry, but there is no escape for you.
 (Screen:  A helicopter appears and fires at the windows, Jill Valentine 
hiding behind the radio.)

79. Negotiate (If you choose ‘Negotiate with Nicholai’)
 (Screen: Jill Valentine grabs the microphone)
Jill Valentine: So, you wanna get out of here alone. Is that your plan?
Nicholai Ginovaef: I made certain that none of the other supervisors 
survived. Since I’’ be the only one who knows what really happened, I’ll have 
more...bargaining power when it comes to discussing my bonus. 
Jill Valentine: Then why kill me? I’m not on their payroll.
Nicholai Ginovaef: Well, they want you eliminated for reasons of their own. 
The amount is modest, but there is a reward to be claimed upon the 
confirmation of your death.
 (Screen: Pause. The radio beeps again.)
Nicholai Ginovaef (the helicopter leaving): Although I’m sure I’ll miss you. 
It’s time to say goodbye. You can either accept death with dignity or die 
with regret. It’s entirely up to you.
 (Screen: The helicopter leaves. Carlos Oliviera enters the radio room.)
Carlos Oliviera: Jill, what happened? (walks up to her)
Jill Valentine: Carlos. Nicholai beat us to the chopper.
 (Screen: Carlos Oliviera looks outside.)
Carlos Oliviera: I guess this is it then. But I don’t wanna die in a place 
like this! (turns around) This isn’t over yet! I’m not giving up Jill! We 
still have a chance!
 (Screen: Carlos Oliviera walks over to the radio and begins pressing 
buttons. If Jill Valentine tries to talk to him)
Carlos Oliviera: I am not going to give up!
 (Screen: Jill Valentine goes to leave.)
Carlos Oliviera (turns around): Jill, that’s it! We gotta find a way outta 
here now!
 (Screen: Carlos Oliviera runs off. Jill Valentine goes to leave.)
Announcement: Warning. Missile attack confirmed. Warning missile attack 
confirmed. Emergency Level B. All personnel evacuate immediately.
 (Screen:  The shutters slide down and a panel opens up, revealing a ladder.)

80. Destroy (If you choose ‘Return fire to the chopper’)
 (Screen:  Jill Valentine fires back at the helicopter, making it explode. 
The helicopter falls, destroyed. Carlos Oliviera enters the radio room.)
Carlos Oliviera: Jill, what happened? (walks up to Jill Valentine)
Jill Valentine: Carlos...The chopper is...
Screen: Carlos Oliviera looks outside.)
Carlos Oliviera: I guess this is it then. But I don’t wanna die in a place 
like this! (turns around) This isn’t over yet! I’m not giving up Jill! We 
still have a chance!
 (Screen: Carlos Oliviera walks over to the radio and begins pressing 
buttons. If Jill Valentine tries to talk to him)
Carlos Oliviera: I am not going to give up!
 (Screen: Jill Valentine goes to leave.)
Carlos Oliviera (turns around): Jill, that’s it! We gotta find a way outta 
here now!
 (Screen: Carlos Oliviera runs off. Jill Valentine goes to leave.)
Announcement: Warning. Missile attack confirmed. Warning missile attack 
confirmed. Emergency Level B. All personnel evacuate immediately.
 (Screen:  The shutters slide down and a panel opens up, revealing a ladder.)

81. No Escape
 (Screen:  Jill Valentine enters the Rail Cannon testing room. The room 
shakes and the door cracks, making it impossible to open again.)

82. Rail Cannon
 (Screen:  Jill Valentine runs up to the computer next to the rail cannon.)
Computer: Checking...system. (lights turned on at three different batteries) 
Checking...data. Warning. There is not enough power to activate...the 
system.)

83. Nemesis’ Final Form
 (Screen:  Jill Valentine runs to Battery 1 and pushes it in. A red light on 
the computer turns blue.)
Computer: Battery connected.
 (Screen:  Jill Valentine is staring at the back wall where a dead tyrant 
was, stepping back as pieces of flesh fell, then a piece of Nemesis’ body. 
The large piece sprays fluids as it grows and mutates, growing large limbs. 
Nemesis flips over, revealing his new face and roaring.)

84. Full Power
 (Screen:  Jill Valentine avoids Nemesis as she pushes in Battery 2, a red 
light turning blue.)
Computer: Battery connected.
 (Screen:  Jill Valentine runs to Battery 3 and pushes it in, the last red 
light turning blue.)
Computer: Battery connected. Rail Cannon has been...activated. 
Executing...quick charge program. Preparing to fire.
 (Screen:  The room begins to shake as the rail cannon is surrounded by 
electricity. Jill Valentine continues to avoid Nemesis as he sits on a 
garbage pile, shooting acid at her.)
Computer: Five...four...three...two...one...fire.
 (Screen:  The rail cannon fires, clearing a path in the garbage to an exit 
door that was locked.)

85. Nemesis’ Defeat
 (Screen:  The rail cannon fires at Nemesis, who screeches as parts of his 
body are blown off. The smoking remains of his body hit a nearby wall, Jill 
Valentine walking up to him with one arm around her waist.)
Computer: Warning. System overheating. Entering cool down mode.)
 (Screen:  The batteries slide back out as the rail cannon emits smoke.)

86. Determination
 (Screen:  Jill Valentine runs for the unlocked door when she hears a noise. 
She turns around to see a piece of Nemesis, his head, slithering towards 
her.)

87. S.T.A.R.S. (If you choose ‘Exterminate the monster’)
 (Screen:  Nemesis spits acid at Jill Valentine, who rolls away and picks up 
a magnum. Jill Valentine fires at Nemesis, who screams. She gets up and 
continues to fire, walking up to Nemesis.)
Jill Valentine: You want S.T.A.R.S? I’ll give you S.T.A.R.S. (fires one last 
time)
 (Screen:  Nemesis thrashes around as he dissolves, turning into a pile of 
purple-rotted flesh. Jill Valentine leaves the room.)

88. Escape (If you choose ‘Push him off’)
 (Screen:  Jill Valentine exits the building.)
Carlos Oliviera: Jill!
 (Screen:  Jill Valentine sees Carlos Oliviera by an active helicopter.)
Carlos Oliviera (waves arms): Over here!
 (Screen:  Carlos Oliviera and Jill Valentine enter the helicopter and take 
off, Carlos Oliviera flying.)
Jill Valentine: I guess we’re all set.
Carlos Oliviera: Alright then, we’re outta here.
 (Screen:  The helicopter flies by as the missile arrives.)
Jill Valentine: Oh no.
Carlos Oliviera: It’s here. It’s time to go.
 (Screen:  The missile impacts in the center of Raccoon City, a wave of fire 
engulfing the entire city and destroying the streets and the buildings. The 
helicopter flies away as a fiery mushroom cloud blooms, Jill Valentine crying 
out as the helicopter was hit by the shockwave.)
Jill Valentine (looking outside): That’s it. I had it. This time, they’ve 
gone too far.
 (Screen:  The helicopter flies into the sunrise.)

89. Rescue (If you choose ‘Jump off’)
 (Jill Valentine gets off the elevator outside the building. She walks a bit 
before hearing the elevator activate. Carlos Oliviera gets off the elevator.)
Carlos Oliviera: Jill!
Jill Valentine: It’s over, Carlos.
Carlos Oliviera: What are you talking about? Don’t you hear that? There’s a 
second chopper, and it’s here to rescue you!
Jill Valentine: But who is it? Who could possibly be looking for me?
Carlos Oliviera: It doesn’t matter. We just have to be there when it lands.
 (Screen:  Carlos Oliviera runs up a bit and ignites a flare, waving his arms 
as a helicopter appears, landing before them. They board the helicopter and 
it takes off.)
Jill Valentine: Thanks. You saved us.
Barry Burton: I couldn’t let you die.
Jill Valentine: Is...is it you?
 (Screen:  the helicopter flies by as the missile arrives.)
Jill Valentine: It’s coming!
Barry Burton: Yeah. (looks at his watch) It’s the end.
(Screen:  The missile impacts in the center of Raccoon City, a wave of fire 
engulfing the entire city and destroying the streets and the buildings. The 
helicopter flies away as a fiery mushroom cloud blooms, Jill Valentine crying 
out as the helicopter was hit by the shockwave.)
Jill Valentine (looks out the window): That’s it. Umbrella’s going down.
(Screen:  The helicopter flies into the sunrise.)

90. Ending
 (Screen:  The mushroom cloud is frozen.)
Reporter: And now, we have a rather unfortunate turn of events. It seems that 
the president and the federal council have passed judgment over the civilians 
of Raccoon City. The president and the federal council have ruled that the 
bacillus-terminate operation is the best course of action for this extreme 
situation and have since, executed it. Based on that fact, the Raccoon City 
has been literally wiped off the map. Current reports have the death toll 
surpassing the 100,000 mark. Our hearts go out to those poor civilians of 
Raccoon City.
 (Screen:  The color fades, leaving the picture black and white, then fades 
to black.)
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
        status_translated =  speaker.generate_tts(translated, translated_file, 'pt', speaker_path, SPEED, SILENCE_LEFT, SILENCE_RIGHT)
        lyrics.embed(translated, translated_file, 'por')

        # Main audio
        main_file = f"{base_filename}_2_en.mp3"
        status_main = speaker.generate_tts(sentence, main_file, 'en', speaker_path, SPEED,  SILENCE_LEFT, SILENCE_RIGHT)
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

process_text(TEXT_INPUT, f"{NAME}_{SPEAKER_NAME}")
