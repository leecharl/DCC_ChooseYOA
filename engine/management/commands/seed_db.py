from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from engine.models import Adventure, Item, Node, NodeLoot, Option

SEED_ASSETS = Path(__file__).resolve().parent.parent.parent / 'seed_assets'

ADVENTURE_TITLE = 'Level 1: The Collapse'


class Command(BaseCommand):
    help = 'Seeds the database with the "Level 1: The Collapse" adventure (Carl\'s Drop).'

    @transaction.atomic
    def handle(self, *args, **options):
        guitar, _ = Item.objects.get_or_create(
            name='Six-String Smasher',
            defaults={
                'description': 'A battered acoustic guitar radiating a faint, humming magic. Plays like a weapon.',
                'item_type': 'ability',
            },
        )
        shorts, _ = Item.objects.get_or_create(
            name='Enchanted Cargo Shorts of Capacity',
            defaults={
                'description': "Not exactly high fashion, but a hell of a lot better than standing around in your boxers.",
                'item_type': 'armor',
            },
        )

        adventure, _ = Adventure.objects.get_or_create(
            title=ADVENTURE_TITLE,
            defaults={'description': "The building crushed down into the crust of the earth. Carl's Crawl begins."},
        )
        adventure.description = "The building crushed down into the crust of the earth. Carl's Crawl begins."
        if not adventure.cover_image:
            self._attach_image(adventure.cover_image, SEED_ASSETS / 'cover_level1.png')
        adventure.is_published = True
        adventure.save()

        # Seeding is destructive-but-scoped: wipe this adventure's existing story graph
        # (not other adventures, not Users/Runs) so re-running seed_db always produces
        # this exact scenario. Runs pointing at deleted nodes fall back to null via
        # Node.current_node's on_delete=SET_NULL.
        adventure.nodes.all().delete()

        node1 = Node.objects.create(
            adventure=adventure,
            content_text=(
                "The cold was the first thing to hit me. Not the sharp, biting cold of a Seattle winter, "
                "but a wet, claustrophobic chill that clung to my skin like a damp towel.\n\n"
                "My name is Carl. I was twenty-seven years old, a former Coast Guard tech, and as of five "
                "minutes ago, I was holding a tortoiseshell cat in my arms while standing in my boxers, a "
                "leather jacket, and pink Crocs. Then the world ended. The building crushed down into the "
                "crust of the earth, plunging me into a glowing, wrought-iron hellhole.\n\n"
                "I stood in the entry chamber of the dungeon, my heart hammering against my ribs. A "
                "flattened 2025 Corolla was half-buried in the neon-lit cobblestones to my left, crushed "
                "under a massive stone pillar. I clutched Donut tightly to my chest. She was the only thing "
                "I had left of my old life, even if she was a furry, flat-faced monster.\n\n"
                "A robotic voice scraped against my skull.\n\n"
                "NEW ACHIEVEMENT! Loner. You entered the dungeon without any human companions. Didn't "
                "anyone teach you there is safety in numbers? Reward: None! Haha. You are so dead.\n\n"
                "“Yeah, thanks,” I muttered.\n\n"
                "Before I could adjust my grip, the floor beneath Donut vanished. A hidden trapdoor snapped "
                "open, revealing a slick, metal chute. With a startled yowl, she slipped through my arms "
                "and plunged into the dark.\n\n"
                "NEW ACHIEVEMENT! Bad Babysitter. You had one job, Carl. Hold the cat. Now she is lost in a "
                "subterranean death maze. Reward: A crushing sense of guilt! And a Bronze Adventurer Box.\n\n"
                "I stared at the empty space where the cat had been. A holographic map flickered to life in "
                "the bottom corner of my vision. A tiny blue dot blinked in the distance. I was alone, "
                "barefoot, and my cat was currently experiencing the dungeon's version of a trash "
                "compactor. I didn't have time to mourn. I had to move.\n\n"
                "What do you do?"
            ),
        )

        node2 = Node.objects.create(
            adventure=adventure,
            content_text=(
                "The dungeon echoed with a sound I couldn't quite place at first — the harsh clattering "
                "of hard polyurethane wheels on stone.\n\n"
                "They zipped around the corner on rusted, reinforced Razor scooters. Three Caffeinated "
                "Gremlins, their gaunt skin glowing in chemically-induced neon shades of “Synthetic "
                "Taurine Blue” and “Guarana Extract Orange.” Their pupils were dilated into "
                "massive black saucers. They wielded sharpened aluminum selfie-sticks like jousting "
                "lances, vibrating with excess energy.\n\n"
                "What do you do?"
            ),
        )
        self._attach_image(node2.image, SEED_ASSETS / 'node2_gremlins.png')
        node2.save()

        node_death_gremlins = Node.objects.create(
            adventure=adventure,
            is_death=True,
            content_text=(
                "I raised my hands, stepping forward slowly. “Hey, listen — ”\n\n"
                "The gremlins, fueled by 9,000 milligrams of synthetic taurine, did not care about my "
                "de-escalation tactics. One of them did a kickflip off my kneecap, shattering the bone "
                "with a sickening crack. As I collapsed, another jammed a jagged selfie-stick through my "
                "jugular. My vision faded to black as the third gremlin pulled out a cracked smartphone to "
                "film my death."
            ),
        )

        node3 = Node.objects.create(
            adventure=adventure,
            content_text=(
                "Following Donut's blue dot on the minimap, I stumbled through a heavy oak door and into a "
                "designated Safe Zone.\n\n"
                "Instead of a ruined dungeon corridor, the room was a pristine, fully preserved 1920s "
                "speakeasy. Jazz music played softly from a phonograph. A surly Bopca Protector — a "
                "furry, gnome-like creature wearing a sequined flapper dress and a feathered headband — "
                "stood behind a mahogany bar.\n\n"
                "She slid a glowing mocktail across the counter, followed by a wooden loot box left behind "
                "by a crawler who didn't make it.\n\n"
                "I cracked the box open. Inside was the Six-String Smasher, a battered acoustic guitar "
                "radiating a faint, humming magic. Next to it sat a pair of Enchanted Cargo Shorts of "
                "Capacity. They weren't exactly high fashion, but they were a hell of a lot better than "
                "standing around in my boxers. I strapped the guitar to my back, pulled on the shorts, and "
                "downed the drink. The blue dot was moving. I had to keep going."
            ),
        )

        NodeLoot.objects.create(node=node3, item=guitar, message='NEW ACHIEVEMENT: Now You\'re Playing With Power Chords!')
        NodeLoot.objects.create(node=node3, item=shorts, message='NEW ACHIEVEMENT: Pocket Dimension Unlocked!')

        node4 = Node.objects.create(
            adventure=adventure,
            content_text=(
                "The hallway ahead was a bottleneck, blocked by a standard, blue United States Postal "
                "Service collection box. It sat perfectly still under the flickering neon lights, complete "
                "with a faded pickup schedule sticker on the front.\n\n"
                "But as I took a step closer, the bottom of the box split open with a screech of tearing "
                "metal. Eight rusted spider legs erupted from the base. The mail-drop slot snapped open "
                "and shut, revealing rows of jagged, rusty teeth. A Feral Mailbox.\n\n"
                "What do you do?"
            ),
        )
        self._attach_image(node4.image, SEED_ASSETS / 'node4_mailbox.png')
        node4.save()

        node_death_mailbox = Node.objects.create(
            adventure=adventure,
            is_death=True,
            content_text=(
                "I confidently strutted up to the blue metal box and shoved my bare hand into the mail "
                "slot, hoping for a potion or a weapon.\n\n"
                "The mimic activated instantly. The steel slot slammed shut with the force of a hydraulic "
                "press, instantly severing my arm at the elbow. As I fell to my knees, screaming in agony "
                "and spraying blood across the cobblestones, the mailbox sprouted its legs and pounced "
                "directly onto my face."
            ),
        )

        node5 = Node.objects.create(
            adventure=adventure,
            content_text=(
                "I burst through a set of heavy double doors and into the final chamber. The room was a "
                "polished, high-tech nightmare of chrome and mirrors.\n\n"
                "In the center of the room stood a glowing, enchanted pet carrier. Princess Donut was "
                "inside, pacing furiously and spitting. Standing between me and the cat was a ten-foot-tall, "
                "mutated suburbanite wearing perfectly creased khakis and a pastel polo shirt.\n\n"
                "The doors slammed shut behind me. The lights flared Syndicate pink.\n\n"
                "B-B-B-Boss Battle! You have discovered the lair of a Neighborhood Boss! Versus... The "
                "H.O.A. Enforcer, Karen! Level 7 Neighborhood Boss.\n\n"
                "Once a beloved A-list celebrity, Karen peaked in the late 90s and has spent the last three "
                "decades stretching her face so tight she sleeps with her eyes open. Now, she roams the "
                "dungeon demanding to speak to the manager of your existence! Those flowing blonde "
                "extensions? Oh, they aren't synthetic. They are sentient, parasitic dandelions hungry for "
                "flesh, boasting smiles full of sickly yellow teeth that would make a British dentist "
                "weep.\n\n"
                "“I need to speak to the manager of this dungeon!” Karen shrieked, her voice a "
                "high-frequency whistle that made my teeth ache.\n\n"
                "She hurled her massive steel clipboard. It glowed with red energy, slamming into the "
                "floor and creating a glowing 'Violation Notice' trap meant to root me to the spot. "
                "Simultaneously, her dandelion hair stretched across the room, dozens of yellow teeth "
                "snapping wildly at my face.\n\n"
                "How do you survive her onslaught?"
            ),
        )
        self._attach_image(node5.image, SEED_ASSETS / 'node5_karen.png')
        node5.save()

        node_death_karen = Node.objects.create(
            adventure=adventure,
            is_death=True,
            content_text=(
                "I puffed out my chest, planted my feet, and tried to catch the heavy dungeon-steel "
                "clipboard like a baseball.\n\n"
                "It smashed right through my fingers, shattering my hands before embedding itself deep "
                "into my chest. I was instantly rooted to the spot, paralyzed by the magic of the "
                "Violation Notice. Karen shrieked with joy. Her dandelion hair extensions stretched across "
                "the room, wrapping around my limbs. Dozens of sickly yellow mouths latched onto my flesh, "
                "eating me alive while Karen loudly lectured my screaming corpse about leaving my trash "
                "cans out past 8:00 PM."
            ),
        )

        node6_victory = Node.objects.create(
            adventure=adventure,
            is_victory=True,
            content_text=(
                "I dodged the rooting zone, the neon magic sparking against the stones as I closed the "
                "distance. Karen was wide open. Her skin was pulled impossibly, painfully tight across her "
                "skull, looking shiny and waxy under the dungeon lights.\n\n"
                "I didn't hesitate. I threw a right hook, punching her squarely in the nose.\n\n"
                "The impact sounded like a thick rubber band snapping under too much tension. All five of "
                "her magical facelifts failed simultaneously. Her skin pooled down around her neck like a "
                "melting hood, wrapping around her dandelion hair and completely blinding her.\n\n"
                "“My Mayor! I know the Mayor!” she shrieked, stumbling backward and clawing at her "
                "own sagging face.\n\n"
                "She blindly crashed into the glowing pet carrier, shattering the magical lock. The cage "
                "burst open. Donut, absolutely enraged, launched herself like a missile. She landed "
                "squarely on Karen's back and unleashed a point-blank Magic Missile directly into the "
                "monster's skull.\n\n"
                "Karen dropped like a stone. The dungeon rumbled as the heavy iron stairs to Floor 2 "
                "ground into place at the back of the room.\n\n"
                "I wiped the blood off my knuckles and looked down at the cat. “You okay?”\n\n"
                "Donut licked a speck of monster gore off her paw and leveled a furious glare at me. "
                "“That haircut was truly a crime against humanity, Carl. I think we did the dungeon a "
                "favor.”"
            ),
        )

        # Node 1 -> Node 2: both routes converge (the story doesn't branch their outcomes)
        Option.objects.create(from_node=node1, to_node=node2, button_text="Rush blindly down the main, brightly lit corridor toward Donut's dot")
        Option.objects.create(from_node=node1, to_node=node2, button_text='Sneak down the dark, green-lit side alley to look for a safer path')

        # Node 2: The First Blood
        Option.objects.create(from_node=node2, to_node=node3, button_text='Use the Smush skill to leap and stomp them with your pink Crocs')
        Option.objects.create(from_node=node2, to_node=node3, button_text='Stand your ground and throw a right hook')
        Option.objects.create(from_node=node2, to_node=node_death_gremlins, button_text="Hold up your hands and try to reason with them. They're just kids, right?")

        # Node 3: The Safe Room (single path forward)
        Option.objects.create(from_node=node3, to_node=node4, button_text="Follow Donut's blue dot deeper into the dungeon")

        # Node 4: The Mimic Trap
        Option.objects.create(from_node=node4, to_node=node5, button_text='Play a heavy power chord to blast it from a distance', required_item=guitar)
        Option.objects.create(from_node=node4, to_node=node5, button_text='Put your head down and charge right through it')
        Option.objects.create(from_node=node4, to_node=node_death_mailbox, button_text="It's just a mailbox. Walk up and check the drop-slot for loot")

        # Node 5: The Boss Room
        Option.objects.create(from_node=node5, to_node=node6_victory, button_text='Play a heavy metal power chord to shatter the dandelion teeth', required_item=guitar)
        Option.objects.create(from_node=node5, to_node=node6_victory, button_text='Dive behind a ruined topiary bush to avoid the main attack')
        Option.objects.create(from_node=node5, to_node=node_death_karen, button_text='Stand your ground and try to catch the glowing clipboard with your bare hands')

        adventure.start_node = node1
        adventure.save()

        self.stdout.write(self.style.SUCCESS(f'Seeded "{ADVENTURE_TITLE}" ({adventure.nodes.count()} nodes).'))

    def _attach_image(self, field, path):
        if not path.exists():
            return
        with open(path, 'rb') as f:
            field.save(path.name, File(f), save=False)
