import logging
from .exceptions import ConfigurationException
from .conf_str import ConfigurationStr
import oci
import io

logger = logging.getLogger(__name__)


class ConfigurationOCIBucketObject(ConfigurationStr):
    def __init__(self, bucket_name, object_name, client=None, config=None, namespace=None):
        self._oci_client = client
        if client is None and config is None:
            signer = oci.auth.signers.get_resource_principals_signer()
            self._oci_client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
        
        if client is None and not config is None:
            self._oci_client = oci.object_storage.ObjectStorageClient(config)
        
        self._bucket_name = bucket_name
        self._object_name = object_name
        self._oci_namespace = self._oci_client.get_namespace().data if namespace is None else namespace
        stream = ""
        try:
            response = self._oci_client.get_object(self._oci_namespace, self._bucket_name, self._object_name)
            if response.status == 200:
                stream = response.data.content.decode('utf-8')
        except Exception as e:
            if e.code != "ObjectNotFound":
                raise e
            logger.warn(e)
        
        super(ConfigurationOCIBucketObject, self).__init__(stream)
    
    def write(self, output_format='hocon'):
        buffer = io.StringIO()
        super(ConfigurationOCIBucketObject, self).write(buffer, output_format=output_format)
        self._oci_client.put_object(self._oci_namespace, self._bucket_name, self._object_name, buffer.getvalue())
        
        