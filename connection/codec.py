class UnicodeCodec(object):
    @staticmethod
    def encode(data):
        return data.encode('unicode_escape').decode('utf-8')

    @staticmethod
    def decode(data):
        return bytes(data, 'utf-8').decode('unicode_escape')
