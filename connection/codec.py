class UnicodeCodec(object):
    @staticmethod
    def encode(data):
        return data.encode('unicode_escape').decode('utf-8').replace(r'\x', r'\u00')

    @staticmethod
    def decode(data):
        unescaped_unicode = data.encode('utf-8').decode('unicode_escape')
        try:
            unescaped_unicode.encode()
            return unescaped_unicode
        except UnicodeEncodeError:
            return unescaped_unicode.encode('utf-16', 'surrogatepass').decode('utf-16')
