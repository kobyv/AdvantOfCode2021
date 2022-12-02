import binascii
from typing import Tuple
import numpy as np


def hex2bin(hex: str) -> str:
    "returns a string of binary digits"
    b = binascii.unhexlify(hex)
    return "".join([f"{x:08b}" for x in b])

def calc(type_id: int, operands: list[int]):
    if type_id == 0:
        return sum(operands)
    elif type_id == 1:
        return np.prod(operands)
    elif type_id == 2:
        return min(operands)
    elif type_id == 3:
        return max(operands)
    elif type_id == 5:
        assert(len(operands) == 2)
        return 1 if operands[0] > operands[1] else 0
    elif type_id == 6:
        assert(len(operands) == 2)
        return 1 if operands[0] < operands[1] else 0
    elif type_id == 7:
        assert(len(operands) == 2)
        return 1 if operands[0] == operands[1] else 0
    else:
        assert(False)


def parse_packet(d: str, pos: int) -> Tuple[int, int, int]:
    ' Returns (end+1 pos, versions sum, result value for part 2) '
    v = int(d[pos:pos+3], 2)   # version
    t = int(d[pos+3:pos+6], 2)  # type id
    pos += 6
    if t == 4:  # literal value packet type
        value = ""
        while True:
            terminate = d[pos] == "0"
            value += d[pos + 1 : pos + 5]
            pos += 5
            if terminate:
                break
        #pos = ((pos + 3) // 4) * 4
        literal = int(value, 2)
        print('  Version:', v, ' Literal:', literal)
        return (pos, v, literal)
    # operator
    version_sum = v
    print('  OPERATOR:', t, ' version:', v)
    length_type = int(d[pos])  # length type ID: 0=total length, 1=number of sub-packets
    pos += 1
    values: list[int] = []
    if length_type == 0:
        l = int(d[pos:pos+15], 2)
        print('  Length in bytes:', l)
        pos += 15
        pos0 = pos
        while pos-pos0 < l:
            (pos, sub_v, r) = parse_packet(d, pos)
            values.append(r)
            version_sum += sub_v
    else:
        l = int(d[pos:pos+11], 2)
        print('  Length in subpackets:', l)
        pos += 11
        for _ in range(l):
            (pos, sub_v, r) = parse_packet(d, pos)
            values.append(r)
            version_sum += sub_v
    #print('  END')
    result = calc(t, values)
    return (pos, version_sum, result)


# PART 1
#puzzle_input = 'EE00D40C823060'
#puzzle_input = '8A004A801A8002F478'
#puzzle_input = '620080001611562C8802118E34'
#puzzle_input = 'C0015000016115A2E0802F182340'
#puzzle_input = 'A0016C880162017C3686B18A3D4780'
#puzzle_input = "D2FE28"
#puzzle_input = '9C0141080250320F1802104A08'
puzzle_input = '00569F4A0488043262D30B333FCE6938EC5E5228F2C78A017CD78C269921249F2C69256C559CC01083BA00A4C5730FF12A56B1C49A480283C0055A532CF2996197653005FC01093BC4CE6F5AE49E27A7532200AB25A653800A8CAE5DE572EC40080CD26CA01CAD578803CBB004E67C573F000958CAF5FC6D59BC8803D1967E0953C68401034A24CB3ACD934E311004C5A00A4AB9CAE99E52648401F5CC4E91B6C76801F59DA63C1F3B4C78298014F91BCA1BAA9CBA99006093BFF916802923D8CC7A7A09CA010CD62DF8C2439332A58BA1E495A5B8FA846C00814A511A0B9004C52F9EF41EC0128BF306E4021FD005CD23E8D7F393F48FA35FCE4F53191920096674F66D1215C98C49850803A600D4468790748010F8430A60E1002150B20C4273005F8012D95EC09E2A4E4AF7041004A7F2FB3FCDFA93E4578C0099C52201166C01600042E1444F8FA00087C178AF15E179802F377EC695C6B7213F005267E3D33F189ABD2B46B30042655F0035300042A0F47B87A200EC1E84306C801819B45917F9B29700AA66BDC7656A0C49DB7CAEF726C9CEC71EC5F8BB2F2F37C9C743A600A442B004A7D2279125B73127009218C97A73C4D1E6EF64A9EFDE5AF4241F3FA94278E0D9005A32D9C0DD002AB2B7C69B23CCF5B6C280094CE12CDD4D0803CF9F96D1F4012929DA895290FF6F5E2A9009F33D796063803551006E3941A8340008743B8D90ACC015C00DDC0010B873052320002130563A4359CF968000B10258024C8DF2783F9AD6356FB6280312EBB394AC6FE9014AF2F8C381008CB600880021B0AA28463100762FC1983122D2A005CBD11A4F7B9DADFD110805B2E012B1F4249129DA184768912D90B2013A4001098391661E8803D05612C731007216C768566007280126005101656E0062013D64049F10111E6006100E90E004100C1620048009900020E0006DA0015C000418000AF80015B3D938'
d = hex2bin(puzzle_input)
(pos, vsum, result) = parse_packet(d, 0)

print("PART 1 version sum:", vsum)
print("PART 2 result:", result)