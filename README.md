# UHLCS data preprocessing

This codebase contains all the code I used to preprocess Uralic language data from the 
[UHLCS datasets](http://www.ling.helsinki.fi/uhlcs/). 
I used the resulting text datasets for the work described in 

    Unsupervised Learning of Cross-Lingual Symbol Embeddings Without Parallel Data
    Mark Granroth-Wilding and Hannu Toivonen (2019)
    In proceedings of the Society for Computation in Linguistics (SCiL)
   
See [the paper and associated resources](https://mark.granroth-wilding.co.uk/papers/unsup_symbol/) 
for more information about that work.

## Dataset

I can't release the dataset itself, as it's available under license from [the CSC](https://www.csc.fi/).

If you have a non-commercial use for the data, you should be able to get hold of it by 
filling in the CSC's application forms. Then you can use the pipeline defined here 
in `uhlcs_data.conf` to extract UTF-8 text for several languages.

Although the dataset is now hosted and distributed by the CSC, 
[the original webpages](http://www.ling.helsinki.fi/uhlcs/) 
are still available with information about it at the time of writing.

[The CSC's resource can be found here.](http://urn.fi/urn:nbn:fi:lb-201403269)

## Pimlico

The data processing is done using [Pimlico](https://pimlico.readthedocs.io/en/latest/).

To get it running, see [Pimlico's guide](https://pimlico.readthedocs.io/en/latest/guides/bootstrap.html) 
on bootstrapping from a pipeline config file. The config file to run is `uhlcs_data.conf`.
