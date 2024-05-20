import React, { useEffect, useState } from "react";

import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TableSortLabel from "@mui/material/TableSortLabel";

import { ITableRow, ITableColumn, Order } from "./TableUtils";

import { colors } from "../Utils";
import { Checkbox } from "@mui/material";
interface props<T extends ITableRow> {
    columns: Array<ITableColumn<T>>;
    onRequestSort: (event: React.MouseEvent<unknown>, property: keyof T) => void;
    order: Order;
    orderBy: keyof T;
    selectedObj?: Array<string>;
    setSelectedObj?: Function;
    allObj?: Array<string>;
}

export default function EnhancedTableHead<T extends ITableRow>(props: props<T>) {
    const { order, orderBy, onRequestSort } = props;
    const createSortHandler = (property: keyof T) => (event: React.MouseEvent<unknown>) => {
        onRequestSort(event, property);
    };
    const numSelected: number = props.selectedObj ? props.selectedObj.length : 0;
    const rowCount: number = props.allObj ? props.allObj.length : 0;

    return (
        <TableHead>
            <TableRow>
                {props.columns.map((column) => (
                    <TableCell
                        key={column.id.toString()}
                        align={column.align}
                        sortDirection={orderBy === column.id ? order : false}
                        className="tableCell"
                        sx={{ backgroundColor: colors.tertiary, color: "white" }}
                        width={column.width}
                    >
                        {column.headExcluedSort ? (
                            column.id === "checkbox" ? (
                                <Checkbox
                                    color="primary"
                                    indeterminate={numSelected > 0 && numSelected < rowCount}
                                    checked={rowCount > 0 && numSelected === rowCount}
                                    onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                        // console.log(props)
                                        if (props.setSelectedObj) {
                                            if (event.target.checked) {
                                                props.setSelectedObj(props.allObj);
                                            } else {
                                                props.setSelectedObj([]);
                                            }
                                        }
                                    }}
                                />
                            ) : (
                                column.label
                            )
                        ) : (
                            <TableSortLabel
                                active={orderBy === column.id}
                                direction={orderBy === column.id ? order : "desc"}
                                onClick={createSortHandler(column.id)}
                                sx={{
                                    "& .MuiTableSortLabel-icon": { color: "white !important" },
                                    "&.Mui-active": { color: "white" },
                                    "&:hover": { color: "white" },
                                    backgroundColor: colors.tertiary,
                                    color: "white",
                                }}
                            >
                                {column.label}
                            </TableSortLabel>
                        )}
                    </TableCell>
                ))}
            </TableRow>
        </TableHead>
    );
}
