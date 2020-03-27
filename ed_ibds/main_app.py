import edpu.user_interaction
import edpu.pause_at_end
import ed_ibds.collection_scanner
import ed_ibds.collection_file_set
import ed_ibds.collection_compare
import ed_ibds.collection_definition
import ed_ibds.duplicate_finder
import ed_ibds.ibds_utils


def run(user_data):
    def main():
        ACTIONS = [
            'Scan location',
            'Compare all data',
            'Generate collection definitions',
            'Find file duplicates',
            'Check data file set'
        ]

        action = edpu.user_interaction.pick_option('Choose an action', ACTIONS)

        if action == 0:
            storage_device = ed_ibds.ibds_utils.pick_storage_device(user_data.getDeviceList())
            ed_ibds.collection_scanner.scan_storage_device(user_data.getDataPath(), user_data.getCollectionDict(), storage_device)

        elif action == 1:
            ed_ibds.collection_compare.collections(user_data.getDataPath(), user_data.getCollectionDict())

        elif action == 2:
            ed_ibds.collection_definition.generate_collections_definition(user_data.getDataPath(), user_data.getCollectionDict())

        elif action == 3:
            ed_ibds.duplicate_finder.collections_common(user_data.getDataPath(), user_data.getCollectionDict())

        elif action == 4:
            ed_ibds.collection_file_set.check_data_file_set(user_data.getDataPath(), user_data.getCollectionDict())

        else:
            raise Exception('unexpected action')

    edpu.pause_at_end.run(main, 'Program finished successfully')
