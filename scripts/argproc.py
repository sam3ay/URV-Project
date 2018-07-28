import argparse


def parse_args():
    """Parses arguments
    Returns:
        arguments
    Notes:
        Possible subparser addition later. parser.add_subparsers(),
        subparserts.add_parser()
    """
    parser = argparse.ArgumentParser(
            prog='GCStoTSV',
            description='Write to a TSV file'
            )
    parser.add_argument(
            'gcs',
            help='GCS bucket name'
            )
    parser.add_argument(
            'pattern',
            help='Pattern unique to desired files such as file extension',
            )
    parser.add_argument(
            '--metafile',
            action='store_false',
            help='Metadata file exists'
            )
    parser.add_argument(
            '--metadata',
            type=list,
            help='pattern of desired metadata info, location should be in parent \
            folder relative to pattern file',
            nargs='+'
            )
    parser.add_argument(
            '-tsv',
            '--tsv_name',
            default='tsv',
            help='Path to tsv File'
            )
    args = parser.parse_args()
    return vars(args)
