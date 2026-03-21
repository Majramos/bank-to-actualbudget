from bank_to_actualbudget.cli import main


def test_main_outputs_correct_greeting(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out == "Running from bank-to-actualbudget!\n"
