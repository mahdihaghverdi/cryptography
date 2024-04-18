import pathlib
import sys
import rich
from rich.table import Table

sys.path.append(str(pathlib.Path(__file__).parent.parent))
from AES import (
    sub_bytes, get_change_ratio, print_operation_table, shift_row, mix_column, add_round_key, full_round,
    print_pt_ct_diff, print_ct_ct_diff,
)

key = (
    '0011010101101001000001001101101100111100000010011000011101010100'
    '1001110001110101010101001100011101010001101010101100100110111011'
)

pt1 = (
    '0000110011001010010110100100101100111000110000100001001011010101'
    '0111010000011101011111101001001110001000110111000100100101101101'
)

pt2 = (  # first bit is different with `init`
    '1000110011001010010110100100101100111000110000100001001011010101'
    '0111010000011101011111101001001110001000110111000100100101101101'
)


def sb_and_ratio():
    print("SB: Sub Byte")
    ct1 = sub_bytes(pt1)
    print_pt_ct_diff(pt1, ct1, 1)

    ct2 = sub_bytes(pt2)
    print_pt_ct_diff(pt2, ct2, 2)

    count, ratio, diff = get_change_ratio(ct1, ct2)
    print_ct_ct_diff(ct1, ct2)

    print_operation_table('sb', count, ratio)


def sr_and_ratio():
    print("SR: Shift Row")
    ct1 = shift_row(pt1)
    print_pt_ct_diff(pt1, ct1, 1)

    ct2 = shift_row(pt2)
    print_pt_ct_diff(pt2, ct2, 2)

    count, ratio, diff = get_change_ratio(ct1, ct2)
    print_ct_ct_diff(ct1, ct2)

    print_operation_table('sr', count, ratio)


def mc_and_ratio():
    print("MC: Mix Column")
    ct1 = mix_column(pt1)
    print_pt_ct_diff(pt1, ct1, 1)

    ct2 = mix_column(pt2)
    print_pt_ct_diff(pt2, ct2, 2)

    count, ratio, diff = get_change_ratio(ct1, ct2)
    print_ct_ct_diff(ct1, ct2)

    print_operation_table('mc', count, ratio)


def ark_and_ratio():
    print("ARK: Add Round Key")
    ct1 = add_round_key(pt1, key)
    print_pt_ct_diff(pt1, ct1, 1)

    ct2 = add_round_key(pt2, key)
    print_pt_ct_diff(pt2, ct2, 2)

    count, ratio, diff = get_change_ratio(ct1, ct2)
    print_ct_ct_diff(ct1, ct2)

    print_operation_table('ark', count, ratio)


def fr_and_ratio():
    print("FR: Full Round")
    ct1 = full_round(pt1, key)
    print_pt_ct_diff(pt1, ct1, 1)

    ct2 = full_round(pt2, key)
    print_pt_ct_diff(pt2, ct2, 2)

    count, ratio, diff = get_change_ratio(ct1, ct2)
    print_ct_ct_diff(ct1, ct2)

    print_operation_table('fr', count, ratio)


def _():
    print("ON: Op Name")
    rich.print(f'[white]P1[/white]:[bold blue]{"0"*10}[/blue bold]')
    rich.print(f'[white]C1[/white]:[bold magenta]{"1000000001"}[/magenta bold]')
    rich.print(f'[bold red]   [underline]^        ^[/red bold][/underline]')
    print()

    rich.print(f'[white]P2[/white]:[bold blue]{"1"+"0"*9}[/blue bold]')
    rich.print(f'[white]C2[/white]:[bold magenta]0111001110[/magenta bold]')
    rich.print(f'[bold red]   [underline]^^^^  ^^^ [/red bold][/underline]')
    print()

    rich.print(f'[white]C1[/white]:[bold blue]1000000001[/blue bold]')
    rich.print(f'[white]C2[/white]:[bold magenta]0111001110[/magenta bold]')
    rich.print(f'[bold red]   [underline]^^^^  ^^^^[/red bold][/underline]')
    print()

    table = Table("Changed bit No.", 'Bit change ratio', title="ON: Op Name", show_lines=True)
    table.add_row('Cnt', f'[green]8[/green]')
    table.add_row('ratio', f'[bold yellow]80%[/yellow bold]')
    rich.print(table)


if __name__ == '__main__':
    _()
    # sb_and_ratio()
    # print('-' * 131)
    # sr_and_ratio()
    # print('-' * 131)
    # mc_and_ratio()
    # print('-' * 131)
    # ark_and_ratio()
    # print('-' * 131)
    # fr_and_ratio()
