pragma solidity ^0.4.0;

contract Sudoku {
    mapping (string => SudokuField) fields;

    struct SudokuField {
        uint[81] field;
        bool[81] preset;
    }

    function new_game(string id, uint[81] field, bool[81] preset) public {
        fields[id] = SudokuField(field, preset);
    }

    function set_cell(string id, uint cell, uint value) public {
        SudokuField storage sudokuField = fields[id];
        if (sudokuField.preset[cell]) return;
        sudokuField.field[cell] = value;
    }

    function get_field(string id) public constant returns (uint[81] field) {
        return fields[id].field;
    }
}
