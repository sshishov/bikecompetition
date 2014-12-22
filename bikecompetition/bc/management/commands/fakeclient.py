from django.core.management.base import BaseCommand
from optparse import make_option

from bikecompetition.fakeclient import FakeClient


class Command(BaseCommand):
    args = ""
    help = """ Run FakeClient """

    option_list = BaseCommand.option_list + (
        make_option('--competitor_id',
                    dest='competitor_id',
                    help='Competitor ID'),
        make_option('--competition_type',
                    dest='competition_type',
                    help='Competition Type'),
        make_option('--competitor_name',
                    dest='competitor_name',
                    help='Competition Name'),
        make_option('--competition_limit',
                    dest='competition_limit',
                    help='Competition Limit'),
    )

    def handle(self, *args, **options):
        competitor_id = options.get('competitor_id')
        competitor_name = options.get('competitor_name')
        competition_type = options.get('competition_type')
        competition_limit = options.get('competition_limit')

        if (competitor_id is not None or competitor_name is not None) and competition_type is not None:
            FakeClient(id=competitor_id, name=competitor_name, competition_type=competition_type,
                       competition_limit=competition_limit).start()
