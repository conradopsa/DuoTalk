import unittest
import sys
import os

# Add the src directory to the path to import the splitter module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from splitter import split_text_advanced, split_text_safe

class TestSplitTextAdvanced(unittest.TestCase):
    def test_empty(self):
        result = split_text_advanced("")
        self.assertEqual(result, [])

    def test_good_morning_black_mesa(self):
        text = """
        Good morning and welcome to the Black Mesa Transit System. 

        This automated train is provided for the security and convenience of employees of the Black Mesa Research Facility personnel. 
        Please feel free to move about the train or simply sit back and enjoy the ride.
        """

        expect = [
            "Good morning and welcome to", 
            "the Black Mesa Transit System.",
            "This automated train is provided",
            "for the security and convenience",
            "of employees of the Black Mesa Research Facility personnel.",
            "Please feel free to move about",
            "the train or simply sit back",
            "and enjoy the ride."
        ]

        result = split_text_advanced(text)
        print(result)
        self.assertEqual(result, expect)
    
    def test_abreviation(self):
        # text = """
        # Sorry, Mr. Freeman, I’ve got explicit orders not to let you through without your hazard suit on.
        # """

        # expect = [
        #     "Sorry, Mr. Freeman,"
        #     "I’ve got explicit orders not to",
        #     "let you through without your",
        #     "hazard suit on."
        # ]

        # result = split_text_advanced(text)
        # self.assertEqual(result, expect)

        text = """
        Sr. Sra. Mr. Mrs. Dr. Dra. S.T.A.R.S.
        """

        expect = [
            "Sr. Sra. Mr. Mrs. Dr. Dra. S.T.A.R.S."
        ]

        result = split_text_advanced(text)
        
        self.assertEqual(result, expect)

    def test_sorry_mr_freeman_abreviation(self):
        text = """
        Sorry, Mr. Freeman, I’ve got explicit orders not to let you through without your hazard suit on.
        """

        expect = [
            "Sorry, Mr. Freeman, I’ve got explicit orders",
            "not to let you through without your",
            "hazard suit on."
        ]

        result = split_text_advanced(text)
        self.assertEqual(result, expect)

    def test_raccon_city_narrator(self):
        text = """
            01. Raccoon City’s Narrator
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
        """

        expect = [
            '01. Raccoon City’s Narrator', 
            '(Screen: A picture of the Umbrella Corporation’s logo)', 
            'Jill Valentine (Narration): It all began as', 
            'an ordinary day in September...', 
            'An ordinary day in Raccoon City,', 
            'a city controlled by Umbrella.', 
            '(Screen: Jill Valentine’s upper body moving from left-to-right)', 
            'Jill Valentine: No one dared', 
            'to opposed them... and that lack of strength', 
            'would ultimately lead to their destruction.', 
            'I suppose they had to suffer the', 
            'consequences for their actions, but there would', 
            'be no forgiveness.', 
            '(Screen: Jill closes her eyes)', 
            'Jill Valentine: If only they had', 
            'the courage to fight.', 
            'It’s true once the', 
            'wheels of justice began to turn,', 
            'nothing can stop them. Nothing.', 
            '(Screen: Jill sitting on a bed,', 
            'legs crossed, and loading a gun.)', 
            'Jill Valentine: It was Raccoon City’s last', 
            'chance... and my last chance...', 
            'My last escape.'
        ]

        result = split_text_advanced(text)
        self.assertEqual(result, expect)

    def test_train_ride(self):
        text = """
            TRAIN RIDE - EXIT

            Scene: A security guard (“Barney”) opens the door of your train:

            BARNEY: Morning, Mr. Freeman. Looks like you’re running late?
            
            ANOMALOUS MATERIALS
            ANOMALOUS MATERIALS – LOBBY

            Scene: Barney at reception desk.

            BARNEY: Hey, Mr. Freeman—I had a bunch of messages for you, but we had a system crash about twenty minutes ago and I’m still trying to find my files. Just one of those days I guess. They were having some problems down in the test chamber, too, but I think that’s all straightened out. They told me to make sure you headed down there as soon as you got into your hazard suit.
            Scene: If you press button under the reception desk an alarm goes off and guard chastizes you:      
        """

        expect = [
            'TRAIN RIDE - EXIT', 
            'Scene: A security guard (“Barney”) opens', 
            'the door of your train:', 
            'BARNEY: Morning, Mr. Freeman.', 
            'Looks like you’re running late?', 
            'ANOMALOUS MATERIALS', 
            'ANOMALOUS MATERIALS – LOBBY', 
            'Scene: Barney at reception desk.', 
            'BARNEY: Hey, Mr. Freeman—I had', 
            'a bunch of messages for you,', 
            'but we had a system crash about', 
            'twenty minutes ago and I’m still trying', 
            'to find my files.', 
            'Just one of those days I guess.', 
            'They were having some problems down', 
            'in the test chamber, too,', 
            'but I think that’s all straightened out.', 
            'They told me to make sure you', 
            'headed down there as soon as you', 
            'got into your hazard suit.', 
            'Scene: If you press button under', 
            'the reception desk an alarm goes off', 
            'and guard chastizes you:']

        result = split_text_advanced(text)
        
        self.assertEqual(result, expect)

    def test_dormin(self):
        text = "Dormin: Hmm? Thou possesses the Ancient Sword? So thou art mortal..."

        expect = [
            "Dormin: Hmm?", 
            "Thou possesses the Ancient Sword?", 
            "So thou art mortal..."
        ]

        result = split_text_advanced(text)
        self.assertEqual(result, expect)
        
    def test_prologue_sofc(self):
        text = """
        Prologue
        A young man named Wander travels up a mountain astride his horse Agro, carrying with him a cloaked, lifeless body. He comes to a giant bridge extending across a vast and desolate land, connecting the side of the mountain to the top of a large shrine. As he arrives at the building, its door slides up, revealing an enormous spiraling ramp leading to the ground level, and shuts again as Wander passes under it. At the bottom of the ramp is a pool of water, and an entrance to the main chamber. There, sixteen statues line the walls, eight on either side. At the far end of the area is an altar, upon which Wander places the body. He pulls the cloak aside, revealing a woman, Mono, of roughly the same age as him, garbed in a bright white dress. The scene transitions to a shaman mask floating in a stormy sky.

        Man: That place... began from the resonance of intersecting points... They are memories replaced by ens and naught and etched into stone. Blood, young sprouts, sky--and the one with the ability to control beings created from light... In that world, it is said that if one should wish it one can bring back the souls of the dead... ...But to trespass upon that land is strictly forbidden...
        Several shadowed, human-like figures climb out of the ground and approach Wander, prompting him to draw his sword. As Light reflects off of the blade, the creatures retreat, and a voice booms from the large hole in the ceiling.

        Dormin: Hmm? Thou possesses the Ancient Sword? So thou art mortal...
        Wander: Are you Dormin? I was told that in this place at the end of the world--there exists a being who can control the souls of the dead.
        Dormin: Thou art correct... We are the one known as Dormin...
        Wander turns to the woman.
        """
        
        expect = [
            'Prologue', 
            'A young man named Wander travels up', 
            'a mountain astride his horse Agro,', 
            'carrying with him a cloaked, lifeless body.', 
            'He comes to a giant bridge extending', 
            'across a vast and desolate land,', 
            'connecting the side of the mountain', 
            'to the top of a large shrine.', 
            'As he arrives at the building,', 
            'its door slides up, revealing', 
            'an enormous spiraling ramp leading', 
            'to the ground level, and shuts again', 
            'as Wander passes under it.', 
            'At the bottom of the ramp is', 
            'a pool of water, and', 
            'an entrance to the main chamber.',
            'There, sixteen statues line the walls,', 
            'eight on either side.', 
            'At the far end of', 
            'the area is an altar,', 
            'upon which Wander places the body.', 
            'He pulls the cloak aside,', 
            'revealing a woman, Mono, of roughly', 
            'the same age as him,', 
            'garbed in a bright white dress.', 
            'The scene transitions to a shaman mask', 
            'floating in a stormy sky.', 
            'Man: That place... began from', 
            'the resonance of intersecting points...', 
            'They are memories replaced by ens', 
            'and naught and etched into stone.', 
            'Blood, young sprouts, sky--and the one', 
            'with the ability to control beings created from light...', 
            'In that world, it is said', 
            'that if one should wish it one', 
            'can bring back the souls', 
            'of the dead... ...But to trespass upon', 
            'that land is strictly forbidden...', 
            'Several shadowed, human-like figures climb out', 
            'of the ground and approach Wander,', 
            'prompting him to draw his sword.', 
            'As Light reflects off of', 
            'the blade, the creatures retreat,', 
            'and a voice booms from', 
            'the large hole in the ceiling.', 
            'Dormin: Hmm?', 
            'Thou possesses the Ancient Sword?', 
            'So thou art mortal...', 
            'Wander: Are you Dormin?', 
            'I was told that in', 
            'this place at the end', 
            'of the world--there exists a being who', 
            'can control the souls of the dead.', 
            'Dormin: Thou art correct...', 
            'We are the one known as Dormin...', 
            'Wander turns to the woman.'
        ]
        result = split_text_advanced(text)
        print(result)
        self.assertEqual(result, expect)

