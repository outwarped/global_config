import logging
from exceptions import ConfigurationException
from conf_str import ConfigurationStr
import boto3
import io

logger = logging.getLogger(__name__)


class ConfigurationS3(ConfigurationStr):
    def __init__(self, endpoint_url, bucket_name, key, session=None):
        if session is None:
            session = boto3.Session()
        
        s3 = session.resource( 
            's3',
            endpoint_url=endpoint_url,
        )
        self._object = s3.Object(bucket_name, key)
        stream = self._object.get()['Body'].read().decode('utf-8')
        super(ConfigurationS3, self).__init__(stream)
    
    def write(self, output_format='hocon'):
        buffer = io.StringIO()
        super(ConfigurationS3, self).write(buffer, output_format=output_format)
        self._object.put(
            Body = buffer.getvalue()
        )
        
        