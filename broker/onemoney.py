import csv

from .data import Direction, Row, Transaction, row_date, row_value

ONEMONEY_DATE_HEADERS = ["ДАТА"]
ONEMONEY_DIRECTION_HEADERS = ["ТИП"]
ONEMONEY_DIRECTION_MAP: dict[str, Direction] = {
    "Einnahme": "income",
    "Ausgabe": "expense",
    "Überweisung": "transfer",
}
ONEMONEY_SRC_HEADERS = ["VOM KONTO"]
ONEMONEY_DEST_HEADERS = ["ZUM KONTO/ZUR KATEGORIE"]
ONEMONEY_AMOUNT_HEADERS = ["BETRAG"]
ONEMONEY_NOTE_HEADERS = ["NOTIZEN"]


def onemoney_direction(row: Row) -> Direction:
    direction_str = row_value(ONEMONEY_DIRECTION_HEADERS, row)
    try:
        return ONEMONEY_DIRECTION_MAP[direction_str]
    except KeyError as e:
        raise ValueError(f"Unknown direction: {direction_str} (data: {row!r})") from e


def read_onemoney_csv(onemoney_file) -> list[Transaction]:
    reader = csv.DictReader(onemoney_file, quoting=csv.QUOTE_ALL)
    transactions = []
    for row in reader:
        if all(value == "" or value == None for value in row.values()):
            break
        transactions.append(
            Transaction(
                date=row_date(row),
                direction=onemoney_direction(row),
                src=row_value(ONEMONEY_SRC_HEADERS, row),
                dest=row_value(ONEMONEY_DEST_HEADERS, row),
                amount=float(row_value(ONEMONEY_AMOUNT_HEADERS, row)),
                note=row_value(ONEMONEY_NOTE_HEADERS, row),
            )
        )
    return transactions
