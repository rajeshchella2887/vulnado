import React, { useEffect, useState } from "react";

import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableRow from "@mui/material/TableRow";

import { ITableRow, ITableColumn } from "./TableUtils";

import { colors } from "../Utils";

interface props<T extends ITableRow> {
    rowData: Array<T>;
    columns: Array<ITableColumn<T>>;
    handleClick: Function;
    selectedObj?: Array<string>;
    setSelectedObj?: (array: Array<string>) => void;
    selectedObjName?: string;
}

function EnhancedTableRow<T extends ITableRow>(row: T, index: number, props: props<T>) {
    const [selected, setSelected] = useState<boolean>(false);
    // for host
    useEffect(() => {
        if (props.selectedObjName && props.selectedObjName in row) {
            if (
                props.selectedObj &&
                props.selectedObj.includes((row as { [key: string]: any })[props.selectedObjName] as string)
            ) {
                setSelected(true);
            } else {
                setSelected(false);
            }
        }
    }, [props.selectedObj]);

    const handleClick = (row: T, selected: boolean, setSelected: Function) => {
        if (props.selectedObj) {
            props.handleClick(row, props.selectedObj, props?.setSelectedObj);
        } else {
            props.handleClick(row);
        }
        setSelected(!selected);
    };

    return (
        <TableRow
            hover
            tabIndex={-1}
            key={index}
            onClick={(e) => {
                handleClick(row, selected, setSelected);
            }}
            style={{
                backgroundColor: selected ? colors.hover : index % 2 ? colors.primary : colors.secondary,
            }}
            sx={{
                textDecoration: "none",
                "&:hover": { backgroundColor: colors.hover + "!important" },
            }}
        >
            {props.columns.map((column) => {
                const value = row[column.id];
                return (
                    <TableCell
                        key={column.id.toString()}
                        align={column.align}
                        className="tableCell"
                        style={{ color: "white", width: column.width }}
                    >
                        {value && column.format ? column.format(value) : value}
                    </TableCell>
                );
            })}
        </TableRow>
    );
}

export default function EnhancedTableBody<T extends ITableRow>(props: props<T>) {
    return (
        <TableBody>
            {props.rowData.map((row, index) => {
                return EnhancedTableRow(row, index, props);
            })}
        </TableBody>
    );
}
