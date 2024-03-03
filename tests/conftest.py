'''conftest.py: automatic generation of test data based on a specified number of records'''
from decimal import Decimal
from faker import Faker
from app.calculator.operations import Operations as op

fake = Faker()

def generate_test_data(num_records):
    '''Define operation mappings for both Operations and Calculation tests. Also generates test data.'''
    operation_mappings = {
        'add': op.addition,
        'subtract': op.subtraction,
        'multiply': op.multiplication,
        'divide': op.division
    }

    for _ in range(num_records):
        a = Decimal(fake.random_number(digits=2))
        b = Decimal(fake.random_number(digits=2)) if _ % 4 != 3 else Decimal(fake.random_number(digits=1))
        operation_name = fake.random_element(elements=list(operation_mappings.keys()))
        operation_func = operation_mappings[operation_name]

        if operation_func is op.division:
            b = Decimal('1') if b == Decimal('0') else b

        try:
            if operation_func is op.division and b == Decimal('0'):
                expected = "ZeroDivisionError"
            else:
                expected = operation_func(a, b)
        except ZeroDivisionError:
            expected = "ZeroDivisionError"

        yield a, b, operation_name, operation_func, expected

def pytest_addoption(parser):
    '''Adds custom command-line option: --num_records to specify number of tests to generate; default is 5'''
    parser.addoption("--num_records", action="store", default=5, type=int, help="Number of test records to generate")

def pytest_generate_tests(metafunc):
    '''Check if the test is expecting any of the dynamically generated fixtures'''
    if {"a", "b", "expected"}.intersection(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        parameters = list(generate_test_data(num_records))
        modified_parameters = [(a, b, op_name if 'operation_name' in metafunc.fixturenames else op_func, expected) for a, b, op_name, op_func, expected in parameters]
        metafunc.parametrize("a,b,operation,expected", modified_parameters)
