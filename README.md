DNABarcodes
===========

Automated DNA barcode assembly, quality control, and annotation

# Description
`DNABarcodeReader` is designed to automate the steps between obtaining raw DNA sequence data and running phylogenetic/population genetic analyses. The steps include: (1) Creating individual assemblies for each sample in a dataset; (2) Generating quality control reports; (3) Querying local and WWW BLAST databases annotate the barcode with taxonomic information; and (4) Outputting DNA barcode sequence data into a text file in different formats for downstream analyses (e.g., FASTA).

#Prerequisites
##`Python`
`DNABarcodeReader` is is writen in `Python` verstion 2.7+. So, you will need to download and install `Python` if you don't have it already. Information on `Python`, including tutorials can be found [here](http://www.python.org). Installers for Linux, Mac, Windows can be downloaded [here](http://www.python.org/getit/). `DNABarcodeReader` has **NOT** been tested in Windows. Feedback of its use in Linux and Windows would be much appreciated. `DNABarcodeReader` was developed using version 2.7.5 of `Python`.

##`BioPython`
Most of the features of `DNABarcodeReader` are written using the standard modules supplied with a standard `Python` installation. Two additional modules will be needed, however. One is `BioPython`, which includes some of the basic code used to generated sequence output files (e.g., in FASTA format), and some of the functionality needed to run BLAST queries. All the information you will need on `BioPython` can be found [here](http://biopython.org/wiki/Main_Page). Download and installation instructions can be found [here](http://biopython.org/wiki/Download). `DNABarcodeReader` was developed using version 1.62 of `BioPython`.

##ZODB - native object database for `Python`
The second extra module is ZODB, which provides an easy interface to create a database of `Python` objectcs. The database ensures persistence of work, and allows one to grow a project by simply adding new raw data, rather than having to restart from scratch. All information required to download, install, and run ZODB can be found [here](http://www.zodb.org/en/latest/). `DNABarcodeReader` was developed using version 3.10.3 of ZODB.

##`Phred`, `Phrap`, and `Consed`
A core process in generating DNA barcodes consists of producing assemblies of raw DNA sequence data for each individual sample. One of the best assemblers out there, in particular for Sanger sequence data - and soon for NGS type data, is formed by the `Phred`, `Phrap`, `Consed` trio. `Phred` (by Brent Ewing) is a base-caller that takes as input raw chromatograms and outputs empirically validated quality scores; `Phrap` (by Phil Green) is an assembler, which takes the ouptut from `Phred` as an input; and `Consed` (by David Gordon) is an assembly visualisation and editting tool. The three tools work on all major computing platforms. All three tools are the intellectual property of the University of Washington. Academic licenses are available for free, but commercial licenses incur a cost.  Instructions on how to obtain a license, download, install, and use `Phred`, `Phrap`, and `Consed` can be found [here](http://www.phrap.org/consed/consed.html#howToGet).

**Only `Phred` and `Phrap` are essential.**

`Consed` is only needed as a post-processing tool, to examine DNA barcodes that do not pass QC. **Even though `Consed` is not needed, we highly recommend its use.**

###References
Ewing, B., Hillier, L., Wendl, M.,  and Green, P., 1998, "Basecalling of automated
         sequencer traces using phred.  I. Accuracy assesment", Genome Research 8: 175-185.

Ewing, B. and Green, P., 1998, "Basecalling of automated sequencer traces using
         phred.  II. Error probabilities", Genome Research 8: 186-194.

Green, P., 1994, Phrap, unpublished.  http://www.phrap.org

Gordon, D., Abajian, C., and Green, P., 1998, "Consed: A grapical tool for sequence
         finishing", Genome Research 8:195-202.

##`PolyPhred`
DNA barcodes are generally designed around a mitochondrial or chloroplast gene. These are haploid genomes, and thus carry the special assumption that there should be no variation within individuals at a particular site. This is convenient from the barcode perspective. Each sample should have a string of unambiguous bases that represent its DNA barcode. When variation does occur, two possible explanations are possible: (1) there is experiment error (e.g., sample was contaminated with DNA from another sample); or (2) there is something biologically interesting happening (e.g., blood sample is infected with multiple lineages of a parasite). `DNABarcodeReader` won't help identify which of these two has occurred, but it will allow you to *optionally* use `PolyPhred` (by Debrah Nickerson) to assess the chance that a sample contains multiple barcodes. `PolyPhred` examines chromatograms for signatures of overlapping peaks.

As in `Phred`,`Phrap`, and `Consed`, we do not distribute `PolyPhred` with `DNABarcodeReader`. `PolyPhred` is the intellectual property of the University of Washington. Academic licenses are available for free, but commercial licenses incur a cost. Instructions on how to obtain a license, download, install, and use [here](http://droog.gs.washington.edu/polyphred/poly_get.html).

###References
Nickerson, D.A., Tobe, V.O., and Taylor, S.L, 1997, "PolyPhred: automating the
         detection and genotyping of single nucleotide substitutions using fluorescence-based
         resequencing", Nucleic Acids Research, 25: 2745-2751.

##NCBI `BLAST`
In some cases, the user may have a specific database that they wish to use to annotate their barcodes. For instance, the user might have a database of barcodes of known organisms in his or her study area; or, they may have a database of organisms that are listed under CITES Appendix I. To be able to query these databases, the user will require at least a FASTA file with all the barcode sequences of interest, with suitable annotation, and a local copy of `BLAST` software. Instructions on how to obtain a copy and install `BLAST` locally can be found [here](http://www.ncbi.nlm.nih.gov/guide/howto/run-blast-local/). All the command line instructions for running `BLAST` locally can be found [here](http://www.ncbi.nlm.nih.gov/books/NBK1763/). However, the user does not need to know any of these commands if he/she wants to use `DNABarcodeReader` as is. They simply need to make sure it is installed.
