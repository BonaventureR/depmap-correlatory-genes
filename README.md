<h1>Depmap Correlatory Genes</h1>


<h2>Description</h2>
This script is used to find genes that are coessential with a given set of genes. It uses the Depmap gene codependency data to find genes that are correlated with the given genes.


<h2>Installation</h2>

Ensure that you have python 3.9 or later installed. This project uses pipenv to manage dependencies. To install the dependencies, run the following command:

```
pip install -r requirements.txt
```

If you would prefer to have the requirements installed in a virtual environment, you can use the following commands:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

<h2>Usage</h2>

Assuming you are at the root of the directory -- to run the script, use the following command:

It helps to move the file containing the genes to process to the root directory `gene_correlation/` and then right click on the file in the file explorer and select "Copy as path" and then run the following command:

```
python src/run.py --file <path to file containing genes to process> --num_genes_to_process <number of genes to process> --threshold <correlation threshold> --num_workers <number of workers for multiprocessing>
```

Example:

```
python src/run.py --file data/test_genes.xlsx --num_genes_to_process 10 --threshold 0.5 --num_workers 10
```

Note: The file containing the genes is the only required argument. The remaining arguments have default values and can be left at their defaults. (threshold is None, num_workers = 10, num_genes_to_process = 50)


<h2>Output</h2>
The output is a csv file containing the following columns:

- gene: the gene that was processed
- coessentiality_genes: a list of the remaining genes that are coessential with the gene that was processed

Assuming you've run the script in the root directory, the output file will be saved to ```output/depmap_gene_correlation_data_<timestamp>.csv```.