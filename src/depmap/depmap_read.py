
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import OrderedDict
from functools import lru_cache
import io
import os
import requests

import pandas as pd
import time as time

SAVE_OUTPUT_FILE = os.path.join(os.getcwd(), 'output')


class DepmapGeneData:
    def __init__(self):
        self.depmap_gene_url = 'https://depmap.org/portal/gene/{gene}/top_correlations?dataset_name=Chronos_Combined'

    def get_depmap_gene_data(self, genes: list[str] = None, num_genes_to_process: int = 50, threshold: float = None, num_workers: int = 10) -> str:
        """Gets correlatory genes for a given set of genes according to depmap coessentiality charts.

        Parameters
        ----------
        genes : list[str], optional
            list of genes to process, by default None
        num_genes_to_process : int, optional
            number of genes to process from the provided screen, by default 50
        threshold : float, optional
            threshold for correlation filter if provided, by default None

        Returns
        -------
        str
            file name of the output csv
        Raises
        ------
        e
            generic exception
        """
        try:
            genes = genes[:num_genes_to_process]
            # preserve order of genes
            output = OrderedDict((gene, None) for gene in genes)

            def process_gene(gene, index):
                coessentiality_df = self.__get_correlation_data_for_gene(gene)
                if coessentiality_df is None:
                    print(f'No coessentiality data found for {gene}')
                    return gene, {'gene': gene, 'coessentiality_genes': []}

                remaining_genes = genes[:index] + genes[index+1:]
                gene_hits = self.find_gene_hits(
                    gene, coessentiality_df, remaining_genes, threshold)
                return gene, {'gene': gene, 'coessentiality_genes': gene_hits}

            with ThreadPoolExecutor(max_workers=min(1, num_workers)) as executor:
                future_to_gene = {executor.submit(
                    process_gene, gene, i): gene for i, gene in enumerate(genes)}
                for future in as_completed(future_to_gene):
                    gene, result = future.result()
                    output[gene] = result

            if not os.path.exists(SAVE_OUTPUT_FILE):
                os.makedirs(SAVE_OUTPUT_FILE)
            file_name = os.path.join(
                SAVE_OUTPUT_FILE, f'depmap_gene_correlation_data_{time.time()}.csv')
            output_df = pd.DataFrame(list(output.values()))
            output_df.to_csv(file_name, index=False)

            return file_name
        except Exception as e:
            print(f'Error getting depmap gene data: {e}')
            raise e

    def find_gene_hits(self, curr_gene: str, coessentiality_df: pd.DataFrame, genes_list: list[str], threshold: float = None) -> list[str]:
        """helper function to find gene hits in coessentiality depmap data compared to all other genes in the screen

        Parameters
        ----------
        curr_gene : str
            gene to process
        coessentiality_df : pd.DataFrame
            coessentiality dataframe for the current gene
        genes_to_process : list[str]
            the remaining genes in the screen
        threshold : float, optional
             threshold for correlation filter if provided, by default None

        Returns
        -------
        list[str]
            list of genes found in the coessentiality data for the current gene
        """
        # Create a boolean mask for genes in the list
        gene_mask = coessentiality_df['Gene'].isin(genes_list)

        if threshold is not None:
            # Apply threshold filter
            gene_mask &= coessentiality_df['Correlation'] > threshold

        # Get the matching genes
        gene_hits = coessentiality_df.loc[gene_mask, 'Gene'].tolist()

        return gene_hits

    @lru_cache(maxsize=256)
    def __get_correlation_data_for_gene(self, gene: str) -> pd.DataFrame:
        """Gets the coessentiality data for a given gene from depmap

        Parameters
        ----------
        gene : str
            gene name

        Returns
        -------
        pd.DataFrame
           dataframe containing the coessentiality data for the given gene

        Raises
        ------
        e
            generic exception
        """
        try:
            gene_correlation_url = self.depmap_gene_url.format(gene=gene)

            with requests.Session() as s:
                download = s.get(gene_correlation_url)
                decoded_content = download.content.decode('utf-8')
                df = pd.read_csv(io.StringIO(decoded_content), delimiter=',')

            return df
        except Exception as e:
            print(f"Error getting gene correlation data for {gene}: {e}")
            raise e


# if __name__ == "__main__":
    # depmap_obj = DepmapGeneData()
    # genes = ['XPR1', 'KIDINS220', 'SOX17', 'XIRP2']
    # depmap_obj.get_depmap_gene_data(genes, threshold=0.5)
