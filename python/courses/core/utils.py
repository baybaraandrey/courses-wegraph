import base64
import tempfile
import uuid

from .constants import QUERY_PARAM_VALUE_LIST_DELIMITER

try:
    import pkg_resources
except ImportError:  # pragma: no cover
    pkg_resources = None


DEFAULT_VERSION = '0.0.0'


def get_version_dumb():
    return DEFAULT_VERSION


def get_version_pkg():
    try:
        return pkg_resources.get_distribution('courses').version
    except pkg_resources.DistributionNotFound:
        return DEFAULT_VERSION


get_version = get_version_pkg if pkg_resources else get_version_dumb


def get_secure_path(n=1):
    return ''.join([
        base64.b64encode(uuid.uuid4().hex.encode('utf-8')).decode()[:-2]
        for _ in range(n)
    ])


def get_base64_url(url):
    return '/'.join(
        map(
            lambda x: base64.b64encode(x.encode('utf-8')).decode()[:-2],
            url.split('/'),
        ),
    )[1:]


def file_from_bytes(bytes_, suffix='.xlsx'):
    t = tempfile.NamedTemporaryFile(suffix=suffix)
    t.write(bytes_)
    t.seek(0)

    return t


def split_query_param_value(value, delimiter=QUERY_PARAM_VALUE_LIST_DELIMITER):
    return value.split(delimiter)
