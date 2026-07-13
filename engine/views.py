from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Adventure, Node, Option, Run


def landing(request):
    """Landing page: login + register forms side by side."""
    if request.user.is_authenticated:
        return redirect('hub')

    login_form = AuthenticationForm()
    register_form = UserCreationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                return redirect('hub')
        elif 'register_submit' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('hub')

    return render(request, 'engine/landing.html', {
        'login_form': login_form,
        'register_form': register_form,
    })


@login_required
def hub(request):
    """Dashboard: published Adventures + the user's Runs."""
    adventures = Adventure.objects.filter(is_published=True)
    runs = request.user.runs.select_related('adventure').order_by('-updated_at')
    return render(request, 'engine/hub.html', {
        'adventures': adventures,
        'runs': runs,
    })


@login_required
def start_run(request, adventure_id):
    """Create a new Run for this adventure and drop the player at its start node."""
    adventure = get_object_or_404(Adventure, id=adventure_id, is_published=True)
    run = Run.objects.create(
        user=request.user,
        adventure=adventure,
        current_node=adventure.start_node,
        status='in_progress',
    )
    return redirect('play_node', run_id=run.id, node_id=run.current_node.id)


@login_required
def play_node(request, run_id, node_id):
    run = get_object_or_404(Run, id=run_id, user=request.user)
    node = get_object_or_404(Node, id=node_id, adventure=run.adventure)

    # Security check: ensure the user is actually on this node
    if run.current_node_id != node.id:
        return redirect('play_node', run_id=run.id, node_id=run.current_node_id)

    ai_message = None

    if node.is_death:
        run.inventory.clear()
        run.status = 'dead'
        run.save()
        ai_message = (
            "NEW ACHIEVEMENT! You Failed a Choose Your Own Adventure. "
            "You read the options. You clicked a button. It was the wrong button. "
            "You tried. You failed. Wow... Just try again. Or don't. "
            "We took all your shiny new toys away."
        )
    elif node.is_victory:
        run.status = 'completed'
        run.save()
        ai_message = "NEW ACHIEVEMENT! You Survived... For Now."
    else:
        for loot in node.loot_drops.select_related('item').all():
            if loot.item not in run.inventory.all():
                run.inventory.add(loot.item)
                ai_message = loot.message

    options = node.options.all()
    inventory_items = run.inventory.all()
    for option in options:
        option.disabled = bool(option.required_item and option.required_item not in inventory_items)

    context = {
        'run': run,
        'node': node,
        'options': options,
        'ai_message': ai_message,
    }
    return render(request, 'engine/play_node.html', context)


@require_POST
@login_required
def process_choice(request, run_id, option_id):
    run = get_object_or_404(Run, id=run_id, user=request.user)
    option = get_object_or_404(Option, id=option_id)

    if run.status != 'in_progress' or option.from_node_id != run.current_node_id:
        return redirect('play_node', run_id=run.id, node_id=run.current_node_id)

    if option.required_item and option.required_item not in run.inventory.all():
        return redirect('play_node', run_id=run.id, node_id=run.current_node_id)

    run.current_node = option.to_node
    run.save()
    return redirect('play_node', run_id=run.id, node_id=run.current_node_id)


@login_required
def restart_run(request, run_id):
    """Resets a dead run back to the starting node."""
    run = get_object_or_404(Run, id=run_id, user=request.user)

    run.current_node = run.adventure.start_node
    run.status = 'in_progress'
    run.inventory.clear()
    run.save()

    return redirect('play_node', run_id=run.id, node_id=run.current_node_id)
