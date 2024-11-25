import yaml
import unittest
from config4 import assembler, serializer, interpreter

def commands_for_array(): #Создание массива
    list_of_commands = "('loadc', 55, 10)\n('write', 61, 1)"
    for i in range(2,9):
        list_of_commands = list_of_commands + f"\n('loadc', 55, {i}0)\n('write', 61, {i})"
    return list_of_commands

def commands_for_operations(): #Проведение операций над массивом
    list_of_commands = "('loadc', 55, 1)\n('read', 57)\n('bswap', 33)\n('write', 61, 1)"
    for i in range(2,9):
        list_of_commands = list_of_commands + f"\n('loadc', 55, {i})\n('read', 57)\n('bswap', 33)\n('write', 61, {i})"
    return list_of_commands

class TestAssembler(unittest.TestCase):
    def test_creation_of_array(self):
        file = open('Test_Program_Temp.txt', 'w')
        file.write(commands_for_array())
        file.close()

        assembler('Test_Program_Temp.txt', 'test_output.bin', 'test_log.yaml')
        interpreter('test_output.bin', 'result.yaml', [1,10])

        file = open('result.yaml', 'r')
        result = yaml.safe_load(file)
        file.close()

        expected_result = {'memory':
                               {'address_1': 10, 'address_2': 20, 'address_3': 30, 'address_4': 40, 'address_5': 50,
                                'address_6': 60, 'address_7': 70, 'address_8': 80, 'address_9': 0, 'address_10': 0}
                           }

        self.assertEqual(result, expected_result)

    def test_bswap_on_program(self):
        file = open('Test_Program_Temp.txt', 'w')
        file.write(commands_for_array()+'\n'+commands_for_operations())
        file.close()

        assembler('Test_Program_Temp.txt', 'test_output.bin', 'test_log.yaml')
        interpreter('test_output.bin', 'result.yaml', [1, 10])

        file = open('result.yaml', 'r')
        result = yaml.safe_load(file)
        file.close()

        expected_result = {'memory':
                               {'address_1': 167772160, 'address_2': 335544320, 'address_3': 503316480, 'address_4': 671088640, 'address_5': 838860800,
                                'address_6': 1006632960, 'address_7': 1174405120, 'address_8': 1342177280, 'address_9': 0, 'address_10': 0}
                           }

        self.assertEqual(result, expected_result)



if __name__ == '__main__':
    unittest.main()