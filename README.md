# aws_s3_core
## Description
This is the implementation that is AWS S3 of Boto3, and it can be used to integrate with Flask framework. 
Boto3 AWS S3的實作，可以與Flask整合使用。 

## Version Log
### Version 1 - 2022/11/23 
* Function List: 
  * access_key getter & setter: 抓取/設定 AWS S3 的 Access Key 
  * secret_access_key getter & setter: 抓取/設定 AWS S3 的 Secret Access Key  
  * region getter & setter: 抓取/設定 AWS S3 的 Region  
  * ReInitialization: 重新初始化 awsS3Core  
  * create_bucket: 建立 AWS S3 的 Bucket  
  * delete_bucket: 刪除 AWS S3 的 Bucket  
  * list_buckets: 表列 AWS S3 的 Bucket  
  * uploadFile: 上傳檔案到 AWS S3 至 Bucket   
  * downloadFile: 下載檔案到 AWS S3 至 Bucket  
  * listFiles: 表列 AWS S3 的 Bucket 中的檔案  
  * deleteFile: 刪除 AWS S3 的 Bucket 中的檔案  
  * getFileAWSS3Link: 抓取 AWS S3 的 Bucket 中的檔案的連結  

## How to use
```python
'''
import awsS3Core

AWS_ACCESS_KEY_ID = [YOUR AWS ACCESS KEY in string format]
AWS_SECRET_ACCESS_KEY = [YOUR AWS SECRET ACCESS KEY in strgin format]
REGION = [WHERE IS YOUR S3 REGION in string format]

s3Helper = awsS3Core.awsS3Helper(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION)
'''
```