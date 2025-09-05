import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Amazon S3
AmazonS3_node = glueContext.create_dynamic_frame.from_catalog(
    database="shipping-db",
    table_name="transformed_data",
    transformation_ctx="AmazonS3_node",
)

# Script generated for node Drop Fields
DropFields_node = DropFields.apply(
    frame=AmazonS3_node,
    paths=[
        "customer_name",
    ],
    transformation_ctx="DropFields_node",
)

# Script generated for node Amazon S3
AmazonS3_node = glueContext.write_dynamic_frame.from_options(
    frame=DropFields_node,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://staging-bucket-8b4d11b0/normalized",
        "partitionKeys": [],
    },
    format_options={"compression": "uncompressed"},
    transformation_ctx="AmazonS3_node",
)

job.commit()
