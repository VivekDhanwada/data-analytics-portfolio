import glob
import os

import boto3

from config import S3_BUCKET

s3 = boto3.client("s3")

UPLOADS = [
    ("../data/historical/clean/*.parquet", "raw/historical"),
    ("../data/historical/source/*.*", "raw/historical_source"),
    ("../data/historical/rejects/*.csv", "raw/historical_rejects"),
]


def existing_sizes(prefix):
    sizes = {}
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=S3_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            sizes[obj["Key"]] = obj["Size"]
    return sizes


for pattern, prefix in UPLOADS:
    files = sorted(glob.glob(pattern))
    have = existing_sizes(prefix)
    sent = skipped = total_mb = 0
    for path in files:
        name = os.path.basename(path)
        month = name.split(".")[0]
        key = f"{prefix}/month={month}/{name}"
        size = os.path.getsize(path)
        if have.get(key) == size:
            skipped += 1
            continue
        s3.upload_file(path, S3_BUCKET, key)
        sent += 1
        total_mb += size / 1e6
        print("uploaded", key)
    print(f"--- {prefix}: {len(files)} local files, {sent} uploaded ({total_mb:.0f} MB), {skipped} skipped\n")
