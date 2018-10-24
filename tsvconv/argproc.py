import argparse


def create_parser():
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
            'suffix',
            help='Pattern unique to desired files such as file extension',
            )
    parser.add_argument(
            '--pairsuffix',
            default='_2.fastq'
            help='Pattern unique to desired files such as file extension',
            )
    parser.add_argument(
            'tsv_name',
            default='tsv',
            help='Path to tsv File'
            )
    parser.add_argument(
            '--json',
            help='Path to json file'
            )
    parser.add_argument(
            '--default',
            type=bool,
            default=True,
            help="Use environmental credentials"
            )
    parser.add_arguement(
            '--ubam',
            type=bool,
            default=True,
            help="search for ubam, assumes no external metada file"
            )
    return parser
