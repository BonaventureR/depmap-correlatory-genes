import pandas as pd
from depmap.depmap_read import DepmapGeneData
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argumnet('--file', type=str, help='path to file containing genes to process'))
    parser.add_argument('--num_genes_to_process', type=int, default=50, help='number of genes in file to process (i.e., top 10,20,50)')
    parser.add_argument('--threshold', type=float, default=None, help='threshold for correlation filter')
    parser.add_argument('--num_workers', type=int, default=10, help='number of workers for multiprocessing')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    data = pd.read_excel(args.file)

    depmap_obj = DepmapGeneData()
    output_file_name = depmap_obj.get_depmap_gene_data(data, args.num_genes_to_process, args.threshold, args.num_workers)

    print('Wrote output to: {file_name}'.format(file_name=output_file_name))