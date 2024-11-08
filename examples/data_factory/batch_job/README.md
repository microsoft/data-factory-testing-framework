# Batch Job

This pipeline is an example on how a batch job can be triggered from an Azure Data Factory pipeline.
It configures a set of variables, create a storage container to be used by the batch job, trigger the job, monitors it,
once complete it moves the output files to another storage account and finally deletes the storage container.

![batch_job.png](batch_job.png)
