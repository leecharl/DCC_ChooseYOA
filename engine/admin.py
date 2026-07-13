from django.contrib import admin
from .models import Item, Adventure, Node, Option, NodeLoot, Run

class OptionInline(admin.TabularInline):
    model = Option
    fk_name = 'from_node'
    extra = 2

class NodeLootInline(admin.TabularInline):
    model = NodeLoot
    extra = 1

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'adventure', 'is_death', 'is_victory')
    list_filter = ('adventure', 'is_death', 'is_victory')
    inlines = [NodeLootInline, OptionInline]

admin.site.register(Item)
admin.site.register(Adventure)
admin.site.register(Run)
