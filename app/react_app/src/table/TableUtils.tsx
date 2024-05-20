import React from "react";

export type Order = "asc" | "desc";

export interface ITableRow {}

export interface ITableColumn<T extends ITableRow> {
    id: keyof T;
    label: string | JSX.Element;
    width?: string;
    align?: "center" | "right" | "inherit" | "left" | "justify" | undefined;
    format?: Function;
    headExcluedSort?: boolean;
}

export interface ITableResponse<T extends ITableRow> {
    data: {
        count: number;
        next: string;
        previous: string;
        results: Array<T>;
        current_page: number;
        per_page: number;
        total_pages: number;
        page_range: Array<number>;
    };

    success: boolean;
}
