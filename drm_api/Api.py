class Api:
    def __init__(self, connection_string: str = None):
        self.service = None
        self.connection_string = connection_string
        for pair in connection_string.split(';'):
            part = pair.split('=')
            if part[0] == 'server':
                self.server = part[1]
            elif part[0] == 'secure':
                self.secure = part[1] in ['true', '1', 'yes']
            elif part[0] == 'port':
                self.port = int(part[1])
            elif part[0] == 'path':
                self.path = part[1]
            elif part[0] == 'service':
                self.service = part[1]
            elif part[0] == 'username':
                self.username = part[1]
            elif part[0] == 'password':
                self.password = part[1]

    @property
    def protocol(self):
        return "https" if self.secure else "http"

    @property
    def url(self):
        if not self.port or (self.secure and self.port == '443') or (not self.secure and self.port == '80'):
            return self.server
        return "{0}:{1}".format(self.server, self.port)

    @property
    def _path(self):
        if self.service:
            return "{0}/{1}".format(self.path, self.service)
        return self.path

    @property
    def end_point(self):
        return "{0}://{1}/{2}".format(self.protocol, self.url, self._path)
