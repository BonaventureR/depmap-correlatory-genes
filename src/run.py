import pandas as pd
from depmap.depmap_read import DepmapGeneData
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--file', type=str,
                        help='path to file containing genes to process')
    parser.add_argument('--gene_col', type=str,
                        default='Gene_symbol', help='column name for gene symbols')
    parser.add_argument('--num_genes_to_process', type=int, default=50,
                        help='number of genes in file to process (i.e., top 10,20,50)')
    parser.add_argument('--threshold', type=float, default=None,
                        help='threshold for correlation filter')
    parser.add_argument('--num_workers', type=int, default=10,
                        help='number of workers for multiprocessing')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    file, gene_col = args.file, args.gene_col
    num_genes_to_process, threshold, num_workers = args.num_genes_to_process, args.threshold, args.num_workers
    if file.endswith('.xlsx'):
        data = pd.read_excel(file)
    elif file.endswith('.csv'):
        data = pd.read_csv(file)
    else:
        raise ValueError('File must be an Excel or CSV file')

    if gene_col not in data.columns:
        raise ValueError(
            f'Gene column {gene_col} not found in file, try passing --gene_col with the column name pertaining to the gene')

    genes = data[gene_col].tolist()
    depmap_obj = DepmapGeneData()
    output_file_name = depmap_obj.get_depmap_gene_data(
        genes, num_genes_to_process, threshold, num_workers)

    print('Wrote output to: {file_name}'.format(file_name=output_file_name))
