from rest_framework import renderers


class XlsxRenderer(renderers.BaseRenderer):
    media_type = 'application/octet-stream'
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
