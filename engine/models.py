from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    ITEM_TYPES = [('weapon', 'Weapon'), ('ability', 'Ability'), ('consumable', 'Consumable'), ('armor', 'Armor')]
    name = models.CharField(max_length=100)
    description = models.TextField()
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    def __str__(self): return f"{self.name} ({self.get_item_type_display()})"

class Adventure(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    start_node = models.ForeignKey('Node', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    is_published = models.BooleanField(default=False)
    def __str__(self): return self.title

class Node(models.Model):
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE, related_name='nodes')
    content_text = models.TextField()
    image = models.ImageField(upload_to='nodes/', blank=True, null=True)
    is_death = models.BooleanField(default=False)
    is_victory = models.BooleanField(default=False)
    def __str__(self): return f"Node {self.id}: {self.content_text[:40]}..."

class Option(models.Model):
    from_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='options')
    to_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_options')
    button_text = models.CharField(max_length=200)
    required_item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self): return f"From {self.from_node.id} -> To {self.to_node.id}: {self.button_text}"

class NodeLoot(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='loot_drops')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True, help_text="AI Announcer text for the UI")
    def __str__(self): return f"{self.item.name} at Node {self.node.id}"

class Run(models.Model):
    STATUS_CHOICES = [('in_progress', 'In Progress'), ('dead', 'Dead'), ('completed', 'Completed')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='runs')
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    current_node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    inventory = models.ManyToManyField(Item, blank=True, related_name='runs')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.user.username}'s run of {self.adventure.title} ({self.status})"
