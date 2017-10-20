import time
import docker.errors
from django.core.management.base import BaseCommand, CommandError
from ...models import Paper, Render


class Command(BaseCommand):
    help = 'Rerender all papers'

    def handle(self, *args, **options):
        print("Rendering papers", end='')
        for i, paper in enumerate(Paper.objects.all()):
            paper.render()
            print('.', end='', flush=True)

            # Update render state periodically so we don't create too many
            # containers
            if i % 100 == 99:
                print()
                print("Updating render state...")
                Render.objects.update_state()
                print("Rendering papers", end='')
        print()
        time.sleep(10)
        print("Updating render state...")
        Render.objects.update_state()