import yaml
import unittest
from config4 import assembler, serializer


class TestAssembler(unittest.TestCase):
    def test_loadc(self):
        file = open('test_input.txt', 'w')
        file.write("('loadc', 55, 397)")
        file.close()

        assembler('test_input.txt', 'test_output.bin', 'test_log.yaml')

        with open('test_log.yaml', 'r') as f:
            log_content = yaml.safe_load(f)
            self.assertEqual(log_content['log'], ["loadc a=55 b=397"])

        with open('test_output.bin', 'rb') as f:
            output_content = f.read()
            self.assertEqual(output_content, bytes([0x77, 0x63, 0x00]))

    def test_read(self):
        file = open('test_input.txt', 'w')
        file.write("('read', 57)")
        file.close()

        assembler('test_input.txt', 'test_output.bin', 'test_log.yaml')

        with open('test_log.yaml', 'r') as f:
            log_content = yaml.safe_load(f)
            self.assertEqual(log_content['log'], ["read a=57"])

        with open('test_output.bin', 'rb') as f:
            output_content = f.read()
            self.assertEqual(output_content, bytes([0x39, 0x00, 0x00]))

    def test_write(self):
        file = open('test_input.txt', 'w')
        file.write("('write', 61, 685)")
        file.close()

        assembler('test_input.txt', 'test_output.bin', 'test_log.yaml')

        with open('test_log.yaml', 'r') as f:
            log_content = yaml.safe_load(f)
            self.assertEqual(log_content['log'], ['write a=61 b=685'])

        with open('test_output.bin', 'rb') as f:
            output_content = f.read()
            self.assertEqual(output_content, bytes([0x7D, 0xAB, 0x00]))

    def test_bswap(self):
        file = open('test_input.txt', 'w')
        file.write("('bswap', 33)")
        file.close()

        assembler('test_input.txt', 'test_output.bin', 'test_log.yaml')

        with open('test_log.yaml', 'r') as f:
            log_content = yaml.safe_load(f)
            self.assertEqual(log_content['log'], ['bswap a=33'])

        with open('test_output.bin', 'rb') as f:
            output_content = f.read()
            self.assertEqual(output_content, bytes([0x21, 0x00, 0x00]))


if __name__ == '__main__':
    unittest.main()