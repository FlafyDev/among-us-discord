from scapy.fields import MSBExtendedField, ConditionalField


class PacketFieldEnum:
    @classmethod
    def as_dict(cls):
        return {
            value: key
            for key, value in vars(cls).items()
            if not key.startswith("_")
            and any(
                (
                    isinstance(value, str),
                    isinstance(value, int),
                    isinstance(value, float),
                    isinstance(value, list),
                    isinstance(value, dict),
                )
            )
        }


class MSBExtendedFieldLenField(MSBExtendedField):
    __slots__ = ["length_of", "count_of", "adjust"]

    def __init__(self, name, default, length_of=None, count_of=None, adjust=lambda pkt, x: x, fld=None):
        MSBExtendedField.__init__(self, name, default)
        self.length_of = length_of
        self.count_of = count_of
        self.adjust = adjust
        if fld is not None:
            self.length_of = fld

    def i2m(self, pkt, x):
        if x is None:
            if self.length_of is not None:
                fld, fval = pkt.getfield_and_val(self.length_of)
                f = fld.i2len(pkt, fval)
            else:
                fld, fval = pkt.getfield_and_val(self.count_of)
                f = fld.i2count(pkt, fval)
            x = self.adjust(pkt, f)
        return x


# noinspection PyAttributeOutsideInit
class SizeAwarePacket:

    def get_expected_size(self):
        return getattr(self, "contentSize") + 3

    def pre_dissect(self, s):
        self.pre_dissect_length = len(s)
        return s

    def post_dissect(self, s):
        self.post_dissect_length = len(s)
        return s

    def extract_padding(self, s):
        expected_size = self.get_expected_size()
        current_size = self.pre_dissect_length - self.post_dissect_length
        padding = expected_size - current_size
        return s[:padding], s[padding:]


def field_switch(mapping, key_extractor):
    result = []
    for key, val in mapping.items():
        field = ConditionalField(val, lambda pkt, key=key: key_extractor(pkt) == key)
        result.append(field)
    return result
