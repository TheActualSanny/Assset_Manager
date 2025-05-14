def formatted_title(file_name: str) -> str:
    '''
        In manager classes' methods where we
        do lookups for certain assets, this method will be
        called to compare the actual names instead of blob names.
    '''
    return file_name.split('_')[1]