import collection_scanner
import edpu.user_interaction
import collection_data
import collection_compare
import collection_definition
import duplicate_finder
import edpu.pause_at_end


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
        storage_device = collection_data.pick_storage_device()
        collection_scanner.scan_storage_device(storage_device)

    elif action == 1:
        collection_compare.collections()

    elif action == 2:
        collection_definition.generate_collections_definition()

    elif action == 3:
        duplicate_finder.collections_common()

    elif action == 4:
        collection_data.check_data_file_set()

    else:
        raise Exception('unexpected action')


edpu.pause_at_end.run(main, 'Program finished successfully')
