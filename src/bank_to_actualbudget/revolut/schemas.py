from typing import TypedDict


class ActualTransactionsFields(TypedDict):
    date: list[str]
    payee: list[str]
    notes: list[str]
    inflow: list[str]
    outflow: list[str]


INPUT_COLUMNS_MAPPINGS: dict[str, str] = {
    "Tipo": "payment_type",
    "Produto": "account_type",
    "Data de Conclusão": "movement_date",
    "Descrição": "description",
    "Montante": "amount",
    "Comissão": "fee",
    "Moeda": "currency",
}


PAYMENT_TYPE_MAPPING: dict[str, str] = {
    "Transferência": "Transfer",
    "Pagamento com cartão": "Payment",
    "Juros": "Interest",
    "ATM": "ATM",
}

ACCOUNT_TYPE_MAPPING: dict[str, str] = {
    "Atual": "revolut",
    "Depósito": "revolut_savings",
}

DESCRIPTION_MAPPING: dict[str, str] = {
    "To Robo portfolio": "Revolut Investing",
    "De EUR Savings": "Revolut Savings",
    "Para EUR Savings": "Revolut Savings",
    "Net Interest Paid to 'Savings'": "Interest",
}
