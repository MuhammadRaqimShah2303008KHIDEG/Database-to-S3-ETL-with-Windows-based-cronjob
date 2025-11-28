# Database-to-S3-ETL-with-Windows-based-cronjob
A scheduled ETL process is configured on a Windows server using a cron-like Task Scheduler job that automatically extracts data from the database at fixed intervals. The job runs a Python/PowerShell script that queries the database, transforms or validates the results, and uploads the output files to S3 bucket for storage or downstream processing
