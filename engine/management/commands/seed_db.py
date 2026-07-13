from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from engine.models import Adventure, Item, Node, NodeLoot, Option

SEED_ASSETS = Path(__file__).resolve().parent.parent.parent / 'seed_assets'


class Command(BaseCommand):
    help = 'Seeds the database with the "Level 1: The Collapse" starter adventure.'

    @transaction.atomic
    def handle(self, *args, **options):
        item, _ = Item.objects.get_or_create(
            name='Spiked Table Leg',
            defaults={
                'description': 'A jagged length of table leg, still trailing a few screws. Surprisingly lethal.',
                'item_type': 'weapon',
            },
        )

        adventure, _ = Adventure.objects.get_or_create(
            title='Level 1: The Collapse',
            defaults={'description': 'Your apartment building just became a dungeon. Welcome to the Crawl.'},
        )
        if not adventure.cover_image:
            self._attach_image(adventure.cover_image, SEED_ASSETS / 'cover_level1.png')
        adventure.is_published = True
        adventure.save()

        if adventure.nodes.exists():
            self.stdout.write(self.style.WARNING('"Level 1: The Collapse" already has nodes; skipping story seed.'))
            self.stdout.write(self.style.SUCCESS('Seed check complete.'))
            return

        node1 = Node.objects.create(
            adventure=adventure,
            content_text=(
                "You are standing in the ruins of your apartment. The walls have been replaced by "
                "damp dungeon stone, and a floating, chittering audience of alien viewers is somehow "
                "already watching your every move. Something glints in the rubble near your feet."
            ),
        )
        self._attach_image(node1.image, SEED_ASSETS / 'node_apartment.png')
        node1.save()

        NodeLoot.objects.create(
            node=node1,
            item=item,
            message='NEW ACHIEVEMENT: Armed and Underdressed!',
        )

        node2 = Node.objects.create(
            adventure=adventure,
            content_text=(
                "A syndicate guard blocks your path, energy drink cans rattling on his belt. "
                "He doesn't look like he wants to talk this out."
            ),
        )
        self._attach_image(node2.image, SEED_ASSETS / 'node_guard.png')
        node2.save()

        node3 = Node.objects.create(adventure=adventure, content_text='You smashed him.', is_victory=True)
        node4 = Node.objects.create(adventure=adventure, content_text='He vaporizes you.', is_death=True)

        Option.objects.create(from_node=node1, to_node=node2, button_text='Approach the guard')
        Option.objects.create(from_node=node2, to_node=node3, button_text='Smash him', required_item=item)
        Option.objects.create(from_node=node2, to_node=node4, button_text='Seduce him')

        adventure.start_node = node1
        adventure.save()

        self.stdout.write(self.style.SUCCESS('Seeded "Level 1: The Collapse".'))

    def _attach_image(self, field, path):
        if not path.exists():
            return
        with open(path, 'rb') as f:
            field.save(path.name, File(f), save=False)
