import boto3
from botocore.exceptions import ClientError

import string

# * Version 1 of awsS3Core - 2022/11/23
# * Function List:
# *     access_key getter & setter: 抓取/設定 AWS S3 的 Access Key
# *     secret_access_key getter & setter: 抓取/設定 AWS S3 的 Secret Access Key
# *     region getter & setter: 抓取/設定 AWS S3 的 Region
# *     ReInitialization: 重新初始化 awsS3Core
# *     create_bucket: 建立 AWS S3 的 Bucket
# *     delete_bucket: 刪除 AWS S3 的 Bucket
# *     list_buckets: 表列 AWS S3 的 Bucket
# *     uploadFile: 上傳檔案到 AWS S3 至 Bucket 
# *     downloadFile: 下載檔案到 AWS S3 至 Bucket
# *     listFiles: 表列 AWS S3 的 Bucket 中的檔案
# *     deleteFile: 刪除 AWS S3 的 Bucket 中的檔案
# *     getFileAWSS3Link: 抓取 AWS S3 的 Bucket 中的檔案的連結

class awsS3Helper():
    def __init__(self, access_key, secret_access_key, region):
        self._access_key = access_key # aws_s3_access_key
        self._secret_access_key = secret_access_key # aws_s3_secret_key
        self._region = region # aws_s3_region
        # * Region of AWS S3 is only support:
        # *         1. US East (N. Virginia) - us-east-1,
        # *         2. US West (N. California) - us-west-1,
        # *         3. US West (Oregon) - us-west-2,
        # *         4. Asia Pacific (Singapore) - ap-southeast-1,
        # *         5. Asia Pacific (Sydney) - ap-southeast-2,
        # *         6. Asia Pacific (Tokyo) - ap-northeast-1,
        # *         7. Europe (Ireland) - eu-west-1,
        # *         8. South America (São Paulo) - sa-east-1,
        self.s3 = boto3.client(service_name = 's3', 
                                region_name=self._region, 
                                aws_access_key_id=self._access_key,
                                aws_secret_access_key=self._secret_access_key)

    @property
    def access_key(self):
        return self._access_key

    @access_key.setter
    def access_key(self, access_key):
        self._access_key = access_key

    @property
    def secret_access_key(self):
        return self._secret_access_key

    @secret_access_key.setter
    def secret_access_key(self, secret_access_key):
        self._secret_access_key = secret_access_key

    @property
    def region(self):
        # * 取得 AWS S3 的 Region
        # * @return: AWS S3 的 Region
        return self._region

    @region.setter
    def region(self, region):
        # * 設定 AWS S3 的 Region
        # * @param _region: AWS S3 的 Region
        # * @return: True or False
        if region == 'us-east-1' or 'us-west-1' or \
                        'us-west-2' or 'ap-southeast-1' or \
                        'ap-southeast-2' or 'ap-northeast-1' or \
                        'eu-west-1' or 'sa-east-1':
            self._region = region
            return True
        else:
            return False

    def ReInitialization(self):
        # * 初始化 boto3.client 物件
        self.s3 = boto3.client(service_name = 's3', 
                                region_name=self._region, 
                                aws_access_key_id=self._access_key,
                                aws_secret_access_key=self._secret_access_key)

    def create_bucket(self, bucket_name):
        # * 建立新的 bucket
        # * @param bucket_name: 希望建立的 Bucket 名稱
        # 存儲桶名稱必須介於 3（最少）到 63（最多）個字符之間
        if len(bucket_name) < 3 or len(bucket_name) > 63:
            return False
        # 存儲桶名稱只能由小寫字母、數字、句點 (.) 和連字符 (-) 組成
        for i in bucket_name:
            if i == '-' or i in string.islower() or i in string.digits or i == '.':
                pass
            else:
                return False
        # 存儲桶名稱必須以字母或數字開頭和結
        if bucket_name[0] in string.islower() or bucket_name[0] in string.digits:
            pass
        else:
            return False
        if bucket_name[-1] in string.islower() or bucket_name[-1] in string.digits:
            pass
        else:
            return False
        # 存儲桶名稱不得包含兩個相鄰的句點。
        for i in range(len(bucket_name)):
            s1 = bucket_name[i]
            s2 = bucket_name[i+1]
            if s1 == '.' and s2 == '.':
                return False
        # 存儲桶名稱不得採用 IP 地址格式（例如，192.168.5.4）。
        bucket_name_split = bucket_name.split('.')
        if len(bucket_name_split) == 4:
            if bucket_name_split[0] in string.digits and \
                bucket_name_split[1] in string.digits and \
                    bucket_name_split[2] in string.digits and \
                    bucket_name_split[3] in string.digits:
                return False
        # 存儲桶名稱不得以前綴 xn-- 開頭。
        if bucket_name[0:3] == 'xn--':
            return False
        # 存儲桶名稱不得以後綴 -s3alias 結尾。
        if bucket_name[8:] == '-s3alias':
            return False
        try:
            self.s3.create_bucket(bucket_name)
        except ClientError as e:
            return False
        return True

    def delete_bucket(self, bucket_name):
        # * 刪除 bucket
        # * @param bucket_name: 希望刪除的 Bucket 名稱
        # * @return: True or False
        try:
            self.s3.delete_bucket(bucket_name)
        except ClientError as e:
            return False
        return True

    def list_buckets(self):
        # * 列出所有的 bucket
        rtnBucketName = []
        bucketList = self.s3.list_buckets()
        for bucket in bucketList['Buckets']:
            rtnBucketName.append(bucket['Name'])
        return rtnBucketName

    def uploadFile(self, fileName, bucketName, keyName):
        # * @param fileName: 檔案名稱 @ client side
        # *        bucketName: Bucket 名稱
        # *        keyName: Key名稱 @ server side
        # * @return: True or False
        try:
            self.s3.upload_file(fileName, bucketName, keyName)
        except ClientError as e:
            return False
        return True

    def downloadFile(self, fileName, bucketName, keyName):
        # * @param fileName: 檔案名稱 @ client side
        # *        bucketName: Bucket 名稱
        # *        keyName: Key名稱 @ server side
        # * @return: True or False
        try:
            self.s3.upload_file(fileName, bucketName, keyName)
        except ClientError as e:
            return False
        return True

    def listFiles(self, bucket_name):
        # * @param bucket_name: Bucket 名稱
        # * @return: { filename: [fileSize, LastModified] }
        rtnFile = {}
        for obj in self.s3.list_objects_v2(Bucket=bucket_name)['Contents']:
            rtnFile[obj['Key']] = [obj['Size'], obj['LastModified']]
        return rtnFile
    
    def deleteFile(self, bucker_name, keyName):
        # * @param bucker_name: Bucket 名稱
        # *        keyName: Key名稱 @ server side
        # * @return: True or False
        try:
            self.s3.delete_object(Bucket=bucker_name, Key=keyName)
        except ClientError as e:
            return False
        return True

    def getFileAWSS3Link(self, bucketName, keyName):
        # * bucket 需要修改為『允許公有存取權 (儲存貯體設定)』
        # * @param bucketName: Bucket 名稱
        # *       keyName: Key名稱 @ server side
        rtnLinkValue = f'https://{bucketName}.s3.amazonaws.com/{keyName}'
        return rtnLinkValue