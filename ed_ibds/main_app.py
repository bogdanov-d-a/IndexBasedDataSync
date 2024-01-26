from edpu import user_interaction
from edpu import pause_at_end
from . import collection_scanner
from . import collection_file_set
from . import collection_compare
from . import collection_definition
from . import duplicate_finder
from . import ibds_utils


def run(user_data):
    def main():
        ACTIONS = [
            'Scan location',
            'Compare all data',
            'Generate collection definitions',
            'Find file duplicates',
            'Check data file set',
            'Find unique data',
        ]

        action = user_interaction.pick_option('Choose an action', ACTIONS)

        if action == 0:
            storage_device_ = ibds_utils.pick_storage_device(user_data.getDeviceList())
            collection_scanner.scan_storage_device(user_data.getDataPath(), user_data.getCollectionDict(), storage_device_, user_data.getSkipMtime())

        elif action == 1:
            collection_compare.collections(user_data.getDataPath(), user_data.getCollectionDict(), user_data.getCompareOnlyAvailable())

        elif action == 2:
            collection_definition.generate_collections_definition(user_data.getDataPath(), user_data.getCollectionDict())

        elif action == 3:
            duplicate_finder.collections_common(user_data.getDataPath(), user_data.getCollectionDict())

        elif action == 4:
            collection_file_set.check_data_file_set(user_data.getDataPath(), user_data.getCollectionDict())

        elif action == 5:
            collection_compare.collections_by_hash(user_data.getDataPath(), user_data.getCollectionDict())

        else:
            raise Exception('unexpected action')

    pause_at_end.run(main, 'Program completed successfully')
