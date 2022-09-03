# S3 Creation
Create two s3 buckets:
- One for your data with a sub-folder per schema
- One for your Athena query outputs

Note: for json your files must be .json and must have one json entry per row (no commas between rows), e.g.
```json
{"name":"Joe", "age":45}
{"name":"Jan", "age": 38}
```

Insert your files into each subfolder. You can have multiple data files in each sub folder as long as they share a schema.
Athena will read across these files.

# Glue Creation
In AWS Glue, first create a new databse for your project.

Then create a Crawler with the following settings:
- Data source of S3
- Target database of the db setup above
- Under the 'Set output and scheduling' advanced options enable the schema grouping (this will mean that you get one schema per folder) and set 'Table Level' to 2 (so that it will group at the level of first layer of inner folders)

(Your other options: if you dont have schema grouping it will make one schema per file. If you dont set table level to 2 it will try to make one big schema total)

Run your crawler, check the 'Tables' created

# Athena

From the athena console, check your data under the tables, you can click the three dots and select 'Preview Table ' to see some data.

From here you are free to query your data. Run the glue crawler whenever you get a new subfolder or a change in schema.

# Glue ETL
For ETL work, you can write and schedule AWS Glue jobs. These can be used to pre-process your data ahead of athena consumption.

Settings to be careful of:
- Number of workers, defaults to 10, probably too high for small data
- Retries, defaults to > 0. You may not when testing want this
Note: if when doing joins you get a 'cannot resolve column name among ()' then set the 'Job Bookmark' to 'Disable' per http://pause.run/aws/aws-glue-error/