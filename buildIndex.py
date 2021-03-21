import os
import json
from algoliasearch.search_client import SearchClient

APPLICATION_ID = '0AUXOSEYK3'

def readAchievementFiles():
    directory = r'./achievementSets'

    fileContents = []

    for entry in os.scandir(directory):
        if (entry.path.endswith(".json") and entry.is_file()):
            with open(entry.path, 'r') as file:
                data = file.read()
                fileContents.append({ 'data': data })

    return fileContents

def fileContentToIndexable(fileContent):
    # parse file
    data_from_json = json.loads(fileContent['data'])
    data = {
        **data_from_json,
        'objectID': data_from_json['id']
    }

    return data

def mapFileContentsToIndexable(fileContents: list):
    return map(fileContentToIndexable, fileContents)

def main():
    print('Indexing files...')

    client = SearchClient.create(APPLICATION_ID, os.environ['ADMIN_API_KEY'])
    index = client.init_index('dev_BGScribe_Achievements')

    indexableFileData = mapFileContentsToIndexable(readAchievementFiles())

    index.replace_all_objects(indexableFileData)

    print(f'Done.')


if __name__ == "__main__":
    main()
