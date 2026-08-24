""" ... """

from sys import exit as _exit

from utils.string_builder import StringBuilder


def main() -> int:
    """ ... """

    bld, aln = StringBuilder.bld_aln()

    aln("line 0")
    aln("line 1")
    aln("line 2")
    aln("line 3")
    aln("line 4")
    aln("line 5")

    for number in [0, 3, 7]:
        start  = bld.position(number=number)
        finish = bld.position(number=number + 1)
        print(f'start  {start}')
        print(f'finish {finish}')
        chunk = bld.chunk(start=start, finish=finish)
        print(f'number {number}')
        print(f'>{chunk.strip()}<')
        print('-----')

    return 0


if __name__ == "__main__":
    _exit(main())
