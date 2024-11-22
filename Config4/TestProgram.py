def bswap(value):
    return ((value & 0xFF) << 24) | \
        ((value & 0xFF00) << 8) | \
        ((value & 0xFF0000) >> 8) | \
        ((value >> 24) & 0xFF)

def main():
    output = ''
    cont = [1,2,3,4,5,6,7,8]
    for s in cont:
        output += str(s) + ' '
    print('Изначальный массив: ' + output)
    output = ''

    for i in range(len(cont)):
        res = bswap(cont[i])
        cont[i] = res
    for s in cont:
        output += str(s) + ' '
    print('Массив после построчного применения команды bswap: ' + output)

main()